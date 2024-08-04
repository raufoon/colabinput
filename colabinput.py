from IPython.display import display, HTML, Javascript
from google.colab.output import eval_js
import re

varnamefriendly = lambda x: re.sub(r'[^a-zA-Z0-9_]', '', x)

def coinput(description="", **elements):

    if not elements:
        elements["input"] = dict(label="Input: ", type="text")
    if ("type" in elements and isinstance(elements.get("type"),dict)) or ("label" in elements and isinstance(elements.get("label"),dict)):
        pass
    elif "type" in elements or "label" in elements:
        temp = elements
        elements = {}
        elements["input"] = temp
    for element in elements.values():
        if element.get("label") is None:
            element["label"] = "Input: " 
        if element.get("type") is None:
            element["type"] = "text"
    

    for i, (name, element) in enumerate(elements.items()):
        #print(i, element, name)
        element["id"] = f"{element['type']}_{varnamefriendly(element['label'])}_{i+1}"
        element["name"] = name if "name" not in element else element["name"]
    def getHTML(element):
      match element["type"]:
        case "text" | "password" | "email" | "url" | "tel" | "number" | "date" | "time" | "datetime-local" | "month" | "week" | "color" | "search" | "file" | "hidden":
            return f'''<label for="{element['id']}">{element["label"]}</label>
                        <input id="{element['id']}" type="{element['type']}" name="{element['name']}" value="{element.get('value', '')}" />'''
        case "range":
            return f'''<label for="{element['id']}">{element["label"]}</label>
                        <input id="{element['id']}" type="range" name="{element['name']}" 
                               value="{element.get('value', '')}" min="{element.get('min', 0)}" max="{element.get('max', 100)}" oninput="this.nextElementSibling.value = this.value">
                                <output>{element.get('value', '')}</output>'''
        case "select" | "radio" | "checkbox":
            optionsHTML = '\n'.join(
                f'<option value="{option}">{option}</option>' if element["type"] == "select" else
                f'''<input type="{element['type']}" id="{element['id']}_{varnamefriendly(option)}" name="{element['name']}" value="{option}">
                   <label for="{element['id']}_{varnamefriendly(option)}">{option}</label>'''
                for option in element.get("options",[])
            )
            if element["type"] == "select":
                return f'''<label for="{element['id']}">{element["label"]}</label>
                            <select id="{element['id']}" name="{element['name']}">\n{optionsHTML}\n</select>'''
            return f'''<label for="{element['id']}">{element["label"]}</label>\n{optionsHTML}'''
        case "textarea":
            return f'''<label for="{element['id']}">{element["label"]}</label>
                        <textarea id="{element['id']}" name="{element['name']}">{element.get('value', '')}</textarea>'''
        case _:
            return "Unknown element type"

    display(HTML('''<p>'''+description+'''</p>\n'''))
    for element in elements.values():
        display(HTML(getHTML(element)))
    display(HTML('''<button id="submitBtn">Submit</button>\n'''))

    inputValuesJS = ""
    for element in elements.values():
        inputValuesJS += Javascript(f'''
    
    if ("{element["type"]}" === 'radio') {{
    var {element["id"]} = document.querySelector('input[name="{element["name"]}"]:checked');
    var {element["id"]}Value = {element["id"]} ? {element["id"]}.value : "";
    //alert({element["id"]}Value);

    var {element["name"]}radios = document.querySelectorAll('input[name="{element["name"]}"]');
            
    // Loop through each radio button and disable it
    {element["name"]}radios.forEach(radio => {{
        radio.disabled = true;
        radio.style.cssText += style;
    }});
    }} else {{
    var {element["id"]} = document.getElementById("{element["id"]}");
    {element["id"]}.disabled = true; {element["id"]}.style.cssText += style;
    var {element["id"]}Value = {element["id"]}.value ? {element["id"]}.value : "";
    //alert({element["id"]}Value);
    }}

    inputValues.push({element["id"]}Value);
    ''').data

    return eval_js('''
new Promise((resolve) => {
  var submitBtn = document.getElementById("submitBtn");
  submitBtn.onclick = function() {
    submitBtn.parentNode.removeChild(submitBtn);
    var inputValues = [];
    var style = "background-color: #383838; color: #ccc; opacity: 1; border-color: #383838";
    '''+inputValuesJS+'''
    resolve(inputValues.length === 1 ? inputValues[0] : inputValues);
  };
})
''')