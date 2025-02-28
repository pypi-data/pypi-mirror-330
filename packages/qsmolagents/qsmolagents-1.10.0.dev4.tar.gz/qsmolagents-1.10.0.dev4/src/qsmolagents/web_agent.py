from io import BytesIO
from time import sleep
import os
import qhelium
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from qsmolagents import CodeAgent, DuckDuckGoSearchTool, tool
from qsmolagents.agents import ActionStep




class WebAgent(CodeAgent):
    """A class to manage web interactions using qhelium."""

    def __init__(self, model, cdp_url):

        self.qhelium_instructions = """
Use your web_search tool when you want to get Google search results.
Then you can use qhelium to access websites. Don't use qhelium for Google search, only for navigating websites!
Don't bother about the qhelium driver, it's already managed.
We've already ran "from qhelium import *"
Then you can go to pages!
Code:
```py
go_to('github.com/trending')
```<end_code>

You can directly click clickable elements by inputting the text that appears on them.
Code:
```py
click("Top products")
```<end_code>

If it's a link:
Code:
```py
click(Link("Top products"))
```<end_code>

If you try to interact with an element and it's not found, you'll get a LookupError.
In general stop your action after each button click to see what happens on your screenshot.
Never try to login in a page.

To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
Code:
```py
scroll_down(num_pixels=1200) # This will scroll one viewport down
```<end_code>

When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
Just use your built-in tool `close_popups` to close them:
Code:
```py
close_popups()
```<end_code>

You can use .exists() to check for the existence of an element. For example:
Code:
```py
if Text('Accept cookies?').exists():
    click('I accept')
```<end_code>

Proceed in several steps rather than trying to solve the task in one shot.
And at the end, only when you have your answer, return your final answer.
Code:
```py
final_answer("YOUR_ANSWER_HERE")
```<end_code>

If pages seem stuck on loading, you might have to wait, for instance `import time` and run `time.sleep(5.0)`. But don't overuse this!
To list elements on page, DO NOT try code-based element searches like 'contributors = find_all(S("ol > li"))': just look at the latest screenshot you have and read it visually, or use your tool search_item_ctrl_f.
Of course, you can act on buttons like a user would do when navigating.
After each code blob you write, you will be automatically provided with an updated screenshot of the browser and the current browser url.
But beware that the screenshot will only be taken at the end of the whole action, it won't see intermediate states.
Don't kill the browser.
When you have modals or cookie banners on screen, you should get rid of them before you can click anything else.
"""

        self.model = model
        self.driver = self.initialize_driver(cdp_url)

        # Initialize parent class
        super().__init__(
            tools=[DuckDuckGoSearchTool(), self.go_back, self.close_popups, self.search_item_ctrl_f],
            model=self.model,
            additional_authorized_imports=["qhelium"],
            step_callbacks=[self.save_screenshot],
            max_steps=20,
            verbosity_level=1
        )


    def save_screenshot(self, memory_step: ActionStep, agent: CodeAgent) -> None:
        sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
        driver = qhelium.get_driver()
        current_step = memory_step.step_number
        if driver is not None:
            for previous_memory_step in agent.memory.steps:  # Remove previous screenshots from logs for lean processing
                if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                    previous_memory_step.observations_images = None
                    previous_memory_step.observations = previous_memory_step.observations.split("DOM Tree:")[0]

            # Execute the bundled DOM tree script
            script_path = os.path.join(os.path.dirname(__file__), 'scripts/build_dom_tree.js')
            with open(script_path, 'r') as f:
                script = f.read()
            result = driver.execute_script(script)

            # Execute script and get clickable elements
            wrapped_script = f"""
                    let clickable_elements = window.get_clickable_elements();
                    console.log(clickable_elements);
                    return clickable_elements['element_str'];
            """
            result = driver.execute_script(wrapped_script)
            driver.execute_script("window.remove_highlight();");

            # Execute the bundled DOM tree script
            script_path = os.path.join(os.path.dirname(__file__), 'scripts/convert_dom_to_markdown.js')
            with open(script_path, 'r') as f:
                script = f.read()
            result = driver.execute_script(script)

            # Execute script and get clickable elements
            wrapped_script = f"""
                return window.convert_dom_to_markdown;
            """
            clickable_elements = driver.execute_script(wrapped_script)

            
            # Take screenshot
            png_bytes = driver.get_screenshot_as_png()
            driver.execute_script("window.remove_highlight();");
            image = Image.open(BytesIO(png_bytes))
            print(f"Captured a browser screenshot: {image.size} pixels")
            memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists, important!

            # Update observations with DOM tree and current URL
            url_info = f"Current url: {driver.current_url}"
            dom_info = f"DOM Tree:\n{result}"
            clickable_info = f"Clickable elements:\n{clickable_elements}"
            
            memory_step.observations = (
                f"{url_info}\n{dom_info}" if memory_step.observations is None 
                else f"{memory_step.observations}\n{url_info}\n{dom_info}\n{clickable_info}"
            )
            return

    def initialize_driver(self, cdp_url):
        """Initialize the Selenium WebDriver to connect to existing Chrome."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", cdp_url)
        
        driver = webdriver.Chrome(options=chrome_options)
        qhelium.set_driver(driver)

        return qhelium.get_driver()

    def run(self, prompt, stream=False, reset=True, additional_args=None):
        """Run the agent with the given prompt."""
        run_prompt = prompt + self.qhelium_instructions
        try:
            self.python_executor("from qhelium import *", self.state)
            if stream:
                for step in super().run(run_prompt, stream=True, reset=reset, additional_args=additional_args):
                    yield step
            else:
                result = super().run(run_prompt, stream=False, reset=reset, additional_args=additional_args)
                print(result)
                return result
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise

    @tool
    def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
        """
        Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
        Args:
            text: The text to search for
            nth_result: Which occurrence to jump to (default: 1)
        """
        driver = qhelium.get_driver()
        elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
        if nth_result > len(elements):
            raise Exception(f"Match n°{nth_result} not found (only {len(elements)} matches found)")
        result = f"Found {len(elements)} matches for '{text}'."
        elem = elements[nth_result - 1]
        driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        result += f"Focused on element {nth_result} of {len(elements)}"
        return result


    @tool
    def go_back() -> None:
        """Goes back to previous page."""
        driver = qhelium.get_driver()
        driver.back()


    @tool
    def close_popups() -> str:
        """
        Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows! This does not work on cookie consent banners.
        """
        driver = qhelium.get_driver()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()



__all__ = [ 'WebAgent' ]