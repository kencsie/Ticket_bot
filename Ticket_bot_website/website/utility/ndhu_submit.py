from playwright.sync_api import sync_playwright
from twocaptcha import TwoCaptcha
from PIL import Image
import io
import base64

CAPTCHA_API_KEY = 'YOUR_API_KEY'

def submit_reservation(account, rentType, court, date, timeSelection, customTime):
    def find_all_available_times(page, date):
        # Find the index of the specified date column
        headers = page.query_selector_all('#MainContent_Table1 tr:first-child td')
        date_index = None
        for i, header in enumerate(headers):
            header_text = header.inner_text()
            if date in header_text:
                date_index = i
                break

        if date_index is None:
            print(f"No column found for the date {date}")
            return []

        # Select all rows in the table except the header row
        rows = page.query_selector_all('#MainContent_Table1 tr')[1:]

        available_times = []

        for row in rows:
            cells = row.query_selector_all('td')
            if date_index < len(cells):
                cell = cells[date_index]
                button = cell.query_selector('button:has-text("[申請]")')
                if button:
                    # Extract the time range from the button text
                    time_range = button.text_content().strip()
                    available_times.append(time_range)
        # Discard the first button
        return available_times[1:]
    
    def time_to_minutes(time_str):
        # Convert time in HH:MM format to minutes since midnight
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def get_captcha_image(page):
        base64_image = page.evaluate('''() => {
            const img = document.getElementById('imgCaptcha');
            return img.src.split(',')[1];
        }''')
        return base64_image

    def solve_captcha_with_tesseract(base64_image):
        #image_data = base64.b64decode(base64_image)
        #image = Image.open(io.BytesIO(image_data))

        solver = TwoCaptcha(CAPTCHA_API_KEY)
        result = solver.normal(
            file=base64_image,
            numeric=4,
            minLength=5,
            maxLength=5,
            case= True
            )
        return result['code']

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            page.goto("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/Default.aspx", wait_until='networkidle')
            page.fill('#MainContent_TXTUSERNO', account['username'])
            page.fill('#MainContent_TXTPWD', account['password'])
            page.click('#MainContent_Button1')
            
            page.click('#MainContent_Button2')
            page.wait_for_timeout(1000)
            page.select_option('#MainContent_drpkind', rentType)
            page.wait_for_timeout(1000)
            page.select_option('#MainContent_DropDownList1', court)
            page.wait_for_timeout(1000)

            page.evaluate("document.getElementById('MainContent_TextBox1').removeAttribute('readonly')")
            page.fill('#MainContent_TextBox1', date)

            page.click('#MainContent_Button1')
            page.wait_for_timeout(1000)

            # Find all available time slots
            available_times = find_all_available_times(page, date)
            '''if available_times:
                print(f"Available time slots on {date}: {available_times}")
            else:
                print(f"No available time slots found on {date}")'''
            
            if timeSelection == "firstTime":
                first_button = available_times[0]
                page.click(f'button:has-text("{first_button}")')
            else:
                custom_minutes = time_to_minutes(customTime)
                # Find and click the button within the custom time range
                for time_range in available_times:
                    time_text = time_range.replace('[申請]', '').strip()
                    start_time, end_time = time_text.split('~')
                    start_minutes = time_to_minutes(f"{start_time}:00")
                    end_minutes = time_to_minutes(f"{end_time}:00")
                    if start_minutes <= custom_minutes <= end_minutes:
                        page.click(f'button:has-text("{time_range}")')
                        break
            
            
            # Handle captcha after button click
            for attempt in range(5):
                page.wait_for_timeout(2000)
                # Handle captcha after button click
                base64_image = get_captcha_image(page)
                solved_captcha = solve_captcha_with_tesseract(base64_image)
                print(f"Solved Captcha: {solved_captcha}")

                # Fill in the solved captcha
                page.fill('#txtCaptchaValue', solved_captcha)
                # Click the "申請" button
                page.click('button[onclick^="doApp"]')

                # Check for failure message
                failure_message = page.query_selector('div:has-text("驗證碼不通過！")')
                empty_message = page.query_selector('div:has-text("驗證碼未填寫！")')
                if failure_message or empty_message:
                    print(f"Attempt {attempt + 1}: Captcha failed, retrying...")
                    # Refresh the captcha
                    page.click('button[onclick="refreshCaptcha()"]')
                else:
                    print("Captcha passed successfully.")
                    break

                #page.wait_for_timeout(2000)

            
            page.fill('#MainContent_ReasonTextBox1', "租借使用")  # Assuming the captcha input field has id 'txtCaptchaValue'
            page.click('#MainContent_Button4')
            page.wait_for_timeout(3000)

            browser.close()
            return True

        except Exception as e:
            print("An error occurred:", e)
            browser.close()
            return False