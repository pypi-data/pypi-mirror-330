#!/usr/bin/env python
# coding=utf-8
# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
import shutil
from typing import Optional
import asyncio
import threading
from contextlib import asynccontextmanager
import signal

from qsmolagents.agent_types import AgentAudio, AgentImage, AgentText, handle_agent_output_types
from qsmolagents.agents import ActionStep, MultiStepAgent
from qsmolagents.memory import MemoryStep
from qsmolagents.utils import _is_package_available


def pull_messages_from_step(
    step_log: MemoryStep,
):
    """Extract ChatMessage objects from agent steps with proper nesting"""
    import gradio as gr

    if isinstance(step_log, ActionStep):
        # Output the step number
        step_number = f"Step {step_log.step_number}" if step_log.step_number is not None else ""
        yield gr.ChatMessage(role="assistant", content=f"**{step_number}**")

        # First yield the thought/reasoning from the LLM
        if hasattr(step_log, "model_output") and step_log.model_output is not None:
            # Clean up the LLM output
            model_output = step_log.model_output.strip()
            # Remove any trailing <end_code> and extra backticks, handling multiple possible formats
            model_output = re.sub(r"```\s*<end_code>", "```", model_output)  # handles ```<end_code>
            model_output = re.sub(r"<end_code>\s*```", "```", model_output)  # handles <end_code>```
            model_output = re.sub(r"```\s*\n\s*<end_code>", "```", model_output)  # handles ```\n<end_code>
            model_output = model_output.strip()
            yield gr.ChatMessage(role="assistant", content=model_output)

        # For tool calls, create a parent message
        if hasattr(step_log, "tool_calls") and step_log.tool_calls is not None:
            first_tool_call = step_log.tool_calls[0]
            used_code = first_tool_call.name == "python_interpreter"
            parent_id = f"call_{len(step_log.tool_calls)}"

            # Tool call becomes the parent message with timing info
            # First we will handle arguments based on type
            args = first_tool_call.arguments
            if isinstance(args, dict):
                content = str(args.get("answer", str(args)))
            else:
                content = str(args).strip()

            if used_code:
                # Clean up the content by removing any end code tags
                content = re.sub(r"```.*?\n", "", content)  # Remove existing code blocks
                content = re.sub(r"\s*<end_code>\s*", "", content)  # Remove end_code tags
                content = content.strip()
                if not content.startswith("```python"):
                    content = f"```python\n{content}\n```"

            parent_message_tool = gr.ChatMessage(
                role="assistant",
                content=content,
                metadata={
                    "title": f"🛠️ Used tool {first_tool_call.name}",
                    "id": parent_id,
                    "status": "pending",
                },
            )
            yield parent_message_tool

            # Nesting execution logs under the tool call if they exist
            if hasattr(step_log, "observations") and (
                step_log.observations is not None and step_log.observations.strip()
            ):  # Only yield execution logs if there's actual content
                log_content = step_log.observations.strip()
                if log_content:
                    log_content = re.sub(r"^Execution logs:\s*", "", log_content)
                    yield gr.ChatMessage(
                        role="assistant",
                        content=f"{log_content}",
                        metadata={"title": "📝 Execution Logs", "parent_id": parent_id, "status": "done"},
                    )

            # Nesting any errors under the tool call
            if hasattr(step_log, "error") and step_log.error is not None:
                yield gr.ChatMessage(
                    role="assistant",
                    content=str(step_log.error),
                    metadata={"title": "💥 Error", "parent_id": parent_id, "status": "done"},
                )

            # Update parent message metadata to done status without yielding a new message
            parent_message_tool.metadata["status"] = "done"

        # Handle standalone errors but not from tool calls
        elif hasattr(step_log, "error") and step_log.error is not None:
            yield gr.ChatMessage(role="assistant", content=str(step_log.error), metadata={"title": "💥 Error"})

        # Calculate duration and token information
        step_footnote = f"{step_number}"
        if hasattr(step_log, "input_token_count") and hasattr(step_log, "output_token_count"):
            token_str = (
                f" | Input-tokens:{step_log.input_token_count:,} | Output-tokens:{step_log.output_token_count:,}"
            )
            step_footnote += token_str
        if hasattr(step_log, "duration"):
            step_duration = f" | Duration: {round(float(step_log.duration), 2)}" if step_log.duration else None
            step_footnote += step_duration
        step_footnote = f"""<span style="color: #bbbbc2; font-size: 12px;">{step_footnote}</span> """
        yield gr.ChatMessage(role="assistant", content=f"{step_footnote}")
        yield gr.ChatMessage(role="assistant", content="-----")


def stream_to_gradio(
    agent,
    task: str,
    reset_agent_memory: bool = False,
    additional_args: Optional[dict] = None,
):
    """Runs an agent with the given task and streams the messages from the agent as gradio ChatMessages."""
    if not _is_package_available("gradio"):
        raise ModuleNotFoundError(
            "Please install 'gradio' extra to use the GradioUI: `pip install 'qsmolagents[gradio]'`"
        )
    import gradio as gr

    total_input_tokens = 0
    total_output_tokens = 0

    for step_log in agent.run(task, stream=True, reset=reset_agent_memory, additional_args=additional_args):
        # Track tokens if model provides them
        if getattr(agent.model, "last_input_token_count", None) is not None:
            total_input_tokens += agent.model.last_input_token_count
            total_output_tokens += agent.model.last_output_token_count
            if isinstance(step_log, ActionStep):
                step_log.input_token_count = agent.model.last_input_token_count
                step_log.output_token_count = agent.model.last_output_token_count

        for message in pull_messages_from_step(
            step_log,
        ):
            yield message

    final_answer = step_log  # Last log is the run's final_answer
    final_answer = handle_agent_output_types(final_answer)

    if isinstance(final_answer, AgentText):
        yield gr.ChatMessage(
            role="assistant",
            content=f"**Final answer:**\n{final_answer.to_string()}\n",
        )
    elif isinstance(final_answer, AgentImage):
        yield gr.ChatMessage(
            role="assistant",
            content={"path": final_answer.to_string(), "mime_type": "image/png"},
        )
    elif isinstance(final_answer, AgentAudio):
        yield gr.ChatMessage(
            role="assistant",
            content={"path": final_answer.to_string(), "mime_type": "audio/wav"},
        )
    else:
        yield gr.ChatMessage(role="assistant", content=f"**Final answer:** {str(final_answer)}")


class GradioUI:
    """A one-line interface to launch your agent in Gradio with proper async handling"""

    def __init__(self, agent: MultiStepAgent, file_upload_folder: str | None = None):
        if not _is_package_available("gradio"):
            raise ModuleNotFoundError(
                "Please install 'gradio' extra to use the GradioUI: `pip install 'qsmolagents[gradio]'`"
            )
        self.agent = agent
        self.file_upload_folder = file_upload_folder
        self.name = getattr(agent, "name", None)
        self.description = getattr(agent, "description", None)
        self.stop_event = asyncio.Event()
        self.demo = None
        if self.file_upload_folder is not None:
            if not os.path.exists(file_upload_folder):
                os.mkdir(file_upload_folder)

    def interact_with_agent(self, prompt, messages, session_state):
        import gradio as gr

        # Get the agent type from the template agent
        if "agent" not in session_state:
            session_state["agent"] = self.agent

        try:
            messages.append(gr.ChatMessage(role="user", content=prompt))
            yield messages

            for msg in stream_to_gradio(session_state["agent"], task=prompt, reset_agent_memory=False):
                messages.append(msg)
                yield messages

            yield messages
        except Exception as e:
            print(f"Error in interaction: {str(e)}")
            messages.append(gr.ChatMessage(role="assistant", content=f"Error: {str(e)}"))
            yield messages

    def upload_file(self, file, file_uploads_log, allowed_file_types=None):
        """
        Handle file uploads, default allowed types are .pdf, .docx, and .txt
        """
        import gradio as gr

        if file is None:
            return gr.Textbox(value="No file uploaded", visible=True), file_uploads_log

        if allowed_file_types is None:
            allowed_file_types = [".pdf", ".docx", ".txt"]

        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext not in allowed_file_types:
            return gr.Textbox("File type disallowed", visible=True), file_uploads_log

        # Sanitize file name
        original_name = os.path.basename(file.name)
        sanitized_name = re.sub(
            r"[^\w\-.]", "_", original_name
        )  # Replace any non-alphanumeric, non-dash, or non-dot characters with underscores

        # Save the uploaded file to the specified folder
        file_path = os.path.join(self.file_upload_folder, os.path.basename(sanitized_name))
        shutil.copy(file.name, file_path)

        return gr.Textbox(f"File uploaded: {file_path}", visible=True), file_uploads_log + [file_path]

    def log_user_message(self, text_input, file_uploads_log):
        return (
            text_input
            + (
                f"\nYou have been provided with these files, which might be helpful or not: {file_uploads_log}"
                if len(file_uploads_log) > 0
                else ""
            ),
            "",
        )

    async def launch(self, share: bool = False, **kwargs):
        import gradio as gr

        try:
            with gr.Blocks(fill_height=True, fill_width=True, css="footer{display:none !important}") as demo:
                session_state = gr.State({})
                stored_messages = gr.State([])
                file_uploads_log = gr.State([])

                with gr.Row(equal_height=True):
                    # Sidebar column
                    with gr.Column(scale=1, min_width=250):
                        # Agent Info
                        if self.name:
                            gr.Markdown(f"## {self.name}")
                        if self.description:
                            gr.Markdown(self.description)
                        
                        # Agent Controls
                        with gr.Group():
                            gr.Markdown("### Agent Controls")
                            with gr.Row():
                                clear_btn = gr.Button("🗑️ Clear Chat")
                                reset_btn = gr.Button("🔄 Reset Agent")
                        
                        # File Upload Section
                        if self.file_upload_folder is not None:
                            with gr.Group():
                                gr.Markdown("### File Upload")
                                upload_file = gr.File(label="Upload files", file_count="multiple")
                                upload_status = gr.Textbox(label="Upload Status", interactive=False, visible=False)
                                upload_file.change(
                                    self.upload_file,
                                    [upload_file, file_uploads_log],
                                    [upload_status, file_uploads_log],
                                )
                        
                        # Agent Settings
                        with gr.Group():
                            gr.Markdown("### Settings")
                            max_steps = gr.Slider(
                                minimum=1,
                                maximum=10,
                                value=getattr(self.agent, "max_steps", 4),
                                step=1,
                                label="Max Steps",
                                interactive=True
                            )
                            verbosity = gr.Dropdown(
                                choices=["Low", "Medium", "High"],
                                value="Medium",
                                label="Verbosity Level",
                                interactive=True
                            )
                    
                    # Main chat column
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(
                            label="Agent",
                            type="messages",
                            avatar_images=(
                                None,
                                "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/qsmolagents/mascot_smol.png",
                            ),
                            height=600,
                            show_copy_button=True,
                            container=True,
                            fill_height=True,
                        )
                        with gr.Row():
                            text_input = gr.Textbox(
                                lines=2,
                                label="Chat Message",
                                elem_id="chat-input",
                                placeholder="Type your message here...",
                                show_label=False,
                                container=False,
                            )
                            submit_btn = gr.Button("Send", variant="primary")

                # Event handlers
                def clear_chat():
                    return [], []
                
                def reset_agent(session_state):
                    session_state["agent"] = self.agent
                    return session_state, [], []
                
                def update_agent_settings(steps, verbosity, session_state):
                    if "agent" in session_state:
                        session_state["agent"].max_steps = steps
                        session_state["agent"].verbosity_level = {"Low": 0, "Medium": 1, "High": 2}[verbosity]
                    return session_state

                # Clear chat handler
                clear_btn.click(
                    clear_chat,
                    outputs=[stored_messages, chatbot],
                )
                
                # Reset agent handler
                reset_btn.click(
                    reset_agent,
                    inputs=[session_state],
                    outputs=[session_state, stored_messages, chatbot],
                )
                
                # Settings update handler
                max_steps.change(
                    update_agent_settings,
                    inputs=[max_steps, verbosity, session_state],
                    outputs=[session_state],
                )
                verbosity.change(
                    update_agent_settings,
                    inputs=[max_steps, verbosity, session_state],
                    outputs=[session_state],
                )

                # Chat submission handlers
                submit_fn = text_input.submit(
                    self.log_user_message,
                    [text_input, file_uploads_log],
                    [stored_messages, text_input],
                ).then(
                    self.interact_with_agent,
                    [stored_messages, chatbot, session_state],
                    [chatbot],
                )
                
                submit_btn.click(
                    self.log_user_message,
                    [text_input, file_uploads_log],
                    [stored_messages, text_input],
                ).then(
                    self.interact_with_agent,
                    [stored_messages, chatbot, session_state],
                    [chatbot],
                )

            # Store demo instance for cleanup
            self.demo = demo

            # Launch with proper configuration
            demo.launch(
                prevent_thread_lock=True,
                show_error=True,
                root_path="",
                **kwargs
            )

            # Wait for stop event
            await self.stop_event.wait()

            demo.close()

        except Exception as e:
            print(f"Gradio server error: {e}")
            raise

    def run_in_thread(self, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.launch(**kwargs))
        finally:
            loop.close()

        demo.launch(debug=True, share=share, **kwargs)

    def start(self, **kwargs):
        """Launch the Gradio interface in a separate thread"""
        print("Starting Gradio server...")
        self.thread = threading.Thread(target=self.run_in_thread, kwargs=kwargs)
        # self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the Gradio interface gracefully"""
        try:
            print("Stopping Gradio server...")

            # First close the Gradio interface
            if hasattr(self, 'demo') and self.demo is not None:
                import gradio as gr
                # Close any active connections
                if hasattr(self.demo, 'close_all'):
                    self.demo.close_all()
                # Close the server
                self.demo.close()
                self.demo = None

            # Then signal the event to stop the server
            self.stop_event.set()

            # Finally join the thread with timeout
            if hasattr(self, 'thread'):
                self.thread.join(timeout=2.0)
                if self.thread.is_alive():
                    print("Warning: Gradio server thread did not stop within timeout")
        except Exception as e:
            print(f"Error during Gradio server shutdown: {e}")


__all__ = ["stream_to_gradio", "GradioUI"]
