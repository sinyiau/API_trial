import time
import os

# Helper function to clear the screen for a better user experience
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Dictionary to hold all the text content in both languages
TEXT_CONTENT = {
    'zh': {
        "disclaimer": """
======================================================================
免責聲明：此工具僅為根據 H.R. 1 法案和 KFF 分析得出的資訊摘要，
旨在提供一般性指導，不構成法律或福利資格建議。
使用者應諮詢華盛頓特區醫療保健財政部以獲取官方資訊。
======================================================================
        """,
        "lang_prompt": "請選擇您的語言 (Please select your language):\n1. English\n2. 繁體中文\n> ",
        "invalid_choice": "\n無效的選擇，請重新輸入。",
        "step_1_question": "以下哪個華盛頓特區醫療補助 (Medicaid) 群體最能描述您？\n（請選擇您擁有 Medicaid 的主要原因）",
        "step_1_options": [
            "無子女成年人 (Childless Adult)",
            "家長／照顧者 (Parent / Caretaker)",
            "19歲以下兒童 (Child under 19)",
            "年長者（65歲以上）、失明者或殘障人士 (Aged, Blind, or Disabled)",
            "正在接受長期照護或透過殘障豁免計畫獲得服務",
            "已參加聯邦醫療保險儲蓄計畫 (Enrolled in a Medicare Savings Program)"
        ],
        "step_2_question": "新規定有幾項豁免條款。您是否符合以下任何一種情況？",
        "step_2_options": [
            "我正在懷孕，或在過去12個月內曾分娩。",
            "我是一位13歲以下兒童的主要照顧者。",
            "我是一位殘障人士的主要照顧者。",
            "我身體虛弱、經醫生證明無法工作，或有嚴重／複雜的醫療狀況。",
            "我正在參加藥物或酒精成癮治療計畫。",
            "我已符合糧食券 (SNAP) 或貧困家庭臨時援助 (TANF) 的工作要求。",
            "以上皆非。"
        ],
        "result_unlikely_title": "不大可能受影響",
        "result_unlikely_text": "根據新法律，您的醫療補助保險不大可能受到影響。\n新的社區參與（工作）要求通常不適用於因年齡（19歲以下或65歲以上）、失明或殘障而符合 Medicaid 資格的個人。",
        "result_low_risk_title": "低風險，但可能需要採取行動",
        "result_low_risk_text": "根據您的回答，您很可能符合新社區參與（工作）要求的豁免資格。\n然而，您可能需要向特區政府提供文件以證明您的豁免身份。\nKFF 的分析警告，繁瑣的行政程序本身仍可能使人們的保險面臨風險。",
        "result_high_risk_title": "高風險",
        "result_high_risk_text": """根據您的回答，您的 Medicaid 保險將面臨高風險，很可能受到新法律的影響。

- **您必須做什麼：** 為了維持您的保險，您將被要求每月至少完成並報告 80 小時的「社區參與」活動，例如工作、社區服務、職業培訓或教育課程。

- **您必須報告時數：** 您必須向特區政府報告這些時數。KFF 對阿肯色州類似計畫的分析發現，許多人失去保險不是因為他們沒有工作，而是因為他們「不了解工作要求，或覺得證明合規的過程太繁瑣」。

- **報告程序複雜：** 法律要求您在成功投保之前，必須先證明您已符合至少一個月的80小時規定。投保後，您還必須至少每六個月再次核實一次。

- **沒有其他保險安全網：** 如果您因未滿足這些要求而失去 Medicaid，該法律還規定您將沒有資格獲得財務援助（保費稅收抵免）來購買 ACA 市場上的其他健康保險。
        """
    },
    'en': {
        "disclaimer": """
======================================================================
Disclaimer: This tool is an informational summary based on the text of H.R. 1 
and KFF analysis. It is intended for general guidance and is not legal 
or eligibility advice. Users should consult the D.C. Department of 
Health Care Finance for official information.
======================================================================
        """,
        "lang_prompt": "Please select your language:\n1. English\n2. 繁體中文\n> ",
        "invalid_choice": "\nInvalid choice, please try again.",
        "step_1_question": "Which of these D.C. Medicaid groups best describes you?\n(Choose the one that is the main reason you have Medicaid)",
        "step_1_options": [
            "Childless Adult",
            "Parent / Caretaker",
            "Child under 19",
            "Aged (65+), Blind, or Disabled",
            "Receiving Long-Term Care or services through a Disability Waiver",
            "Enrolled in a Medicare Savings Program (like QMB)"
        ],
        "step_2_question": "The new rules have several exemptions. Do any of the following situations apply to you?",
        "step_2_options": [
            "I am pregnant or have given birth in the past 12 months.",
            "I am the main caretaker for a child under age 13.",
            "I am the main caretaker for a disabled person.",
            "I am medically frail, certified by a doctor as unable to work, or have a serious/complex medical condition.",
            "I am participating in a drug or alcohol addiction treatment program.",
            "I already meet the work requirements for SNAP (food stamps) or TANF.",
            "None of the above apply to me."
        ],
        "result_unlikely_title": "Unlikely to be Affected",
        "result_unlikely_text": "Based on the new law, your Medicaid coverage is unlikely to be affected.\nThe new community engagement (work) requirements generally do not apply to individuals who are eligible for Medicaid due to age (under 19 or 65+), blindness, or a disability.",
        "result_low_risk_title": "Low Risk, but Action May Be Needed",
        "result_low_risk_text": "Based on your answer, you likely qualify for an exemption from the new community engagement (work) requirements.\nHowever, you may need to provide documentation to the D.C. government to verify your exemption status.\nThe KFF analysis warns that administrative hurdles can still put people's coverage at risk.",
        "result_high_risk_title": "High Risk",
        "result_high_risk_text": """Based on your answers, your Medicaid coverage is at HIGH RISK of being affected by the new law.

- **What you must do:** To keep your coverage, you will be required to work, volunteer, or participate in an education or job training program for at least 80 hours per month.

- **You must report your hours:** You will have to report these hours to the D.C. government. KFF analysis of a similar program in Arkansas found many people lost coverage not because they weren't working, but because they \"were unaware of the work requirement or found it too onerous to demonstrate compliance\".

- **Reporting is complex:** The law requires you to prove you met the 80-hour rule for at least one month *before* you can enroll, and then verify it again at least every six months.

- **No other insurance help:** If you lose Medicaid for not meeting these requirements, the law also makes you ineligible for financial help (premium tax credits) to buy other health insurance on the ACA Marketplace.
        """
    }
}

def get_user_choice(prompt, options, lang):
    """Generic function to get a validated user choice from a list of options."""
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return choice
            else:
                print(TEXT_CONTENT[lang]["invalid_choice"])
        except ValueError:
            print(TEXT_CONTENT[lang]["invalid_choice"])

def display_result(lang, result_type):
    """Displays the final result based on the user's path."""
    clear_screen()
    title_key = f"result_{result_type}_title"
    text_key = f"result_{result_type}_text"
    print(f"--- {TEXT_CONTENT[lang][title_key]} ---")
    print(TEXT_CONTENT[lang][text_key])
    print("\n-------------------------------------\n")

def step_2_exemptions(lang):
    """Asks the user about exemptions."""
    clear_screen()
    question = TEXT_CONTENT[lang]["step_2_question"]
    options = TEXT_CONTENT[lang]["step_2_options"]
    
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
        
    prompt = f"\n> "
    choice = get_user_choice(prompt, options, lang)

    if choice <= 6: # Any of the exemptions
        display_result(lang, "low_risk")
    else: # None of the above
        display_result(lang, "high_risk")

def step_1_group_selection(lang):
    """Asks the user for their primary Medicaid group."""
    clear_screen()
    print(TEXT_CONTENT[lang]["disclaimer"])
    time.sleep(2) # Give user time to read disclaimer
    clear_screen()

    question = TEXT_CONTENT[lang]["step_1_question"]
    options = TEXT_CONTENT[lang]["step_1_options"]
    
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
        
    prompt = f"\n> "
    choice = get_user_choice(prompt, options, lang)

    if choice in [1, 2]: # Childless Adult or Parent/Caretaker
        step_2_exemptions(lang)
    elif choice in [3, 4, 5, 6]: # Exempt groups
        display_result(lang, "unlikely")

def main():
    """Main function to run the screener."""
    clear_screen()
    
    # Language selection
    while True:
        try:
            lang_choice = int(input(TEXT_CONTENT['en']['lang_prompt']))
            if lang_choice == 1:
                lang = 'en'
                break
            elif lang_choice == 2:
                lang = 'zh'
                break
            else:
                print(TEXT_CONTENT['en']["invalid_choice"])
        except ValueError:
            print(TEXT_CONTENT['en']["invalid_choice"])

    step_1_group_selection(lang)

if __name__ == "__main__":
    main()