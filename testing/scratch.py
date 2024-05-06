import re

def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251" 
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_blank_lines(text):
    """
    Remove blank lines from the given text.

    Args:
    text (str): The input text containing blank lines.

    Returns:
    str: The text with blank lines removed.
    """
    lines = text.split('\n')
    clean_lines = (line.strip() for line in lines if line.strip())
    return ' '.join(clean_lines)


input_text = """
In this position, I optimize Jira request management by delivering efficient daily support services and promptly addressing issues that ensure seamless data integrity and accessibility. To drive maximum customer satisfaction, I provide strategic recommendations and execute innovative solutions that improve business outcomes and surpass customer expectations.

Further, I institute and roll out user-friendly SOPs (Standard Operating Procedures) and training manuals to enable smooth knowledge transfer that empowers team members to perform tasks effectively. In addition, I oversee the development of SharePoint sites, libraries, and lists for increasing organizational productivity. By revamping the organization's SharePoint online presence with an intuitive design, I significantly elevate the user experience.

⭐ Highlights of my accomplishments in this role include:

☛ Resolved issues of internal and external customers on a daily basis through efficient and effective direct technical assistance.
☛ Pioneered comprehensive procedures, training manuals, and SOPs that enhanced organizational efficiency.
☛ Bolstered competitive edge and heightened customer satisfaction by streamlining the SP access request process through automation and eliminating the need for manual email submissions.

Skills:
✔ Jira Request Management ✔ User Permissions Management ✔ Standard Operating Procedures (SOPs) ✔ SharePoint Development ✔ Procedure Design ✔ Process Optimization ✔ Customer Satisfaction ✔ Innovative Solutions ✔ Training and Knowledge Transfer ✔ Team Collaboration
Skills: Agile Methodologies · IT Documentation · Business Process · System Requirements
"""

text_without_emojis = remove_emojis(input_text)
text_without_blank_lines = remove_blank_lines(text_without_emojis)
print(text_without_blank_lines)