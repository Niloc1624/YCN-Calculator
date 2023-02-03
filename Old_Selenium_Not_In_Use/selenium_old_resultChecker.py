import re


def resultValid(driver, result):
    """
    Checks to make sure the result (selenium html object) is top 6 and not combined.
    """
    result_text = result.get_attribute("innerHTML")

    # Make sure the result is top 6
    if not re.match(r"^[1-6]\)", result_text):
        return 0

    # Make sure this is not a combined event
    if "-- Combine --" in result_text:
        return 0

    # Make sure it was not a straight final
    # Can't get this to work so may come back later
    # Update: found a workaround so may delete this comment block...
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])
    # print(result.get_attribute("href"))
    # driver.get(result.get_attribute("href"))
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    # driver.switch_to.window(driver.window_handles[-1])

    return 1
