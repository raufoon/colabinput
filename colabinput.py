# Version 0.2
from IPython.display import display, HTML, Javascript
from google.colab.output import eval_js
import re
import time

_varnamefriendly = lambda x: re.sub(r'[^a-zA-Z0-9_]', '', x)

def coinput(**elements):
    display(Javascript('''// Check if a button with id "EnterBtn" already exists
        var existingButton = document.getElementById("EnterBtn");
        if (existingButton) {
            // Remove the existing button
            existingButton.parentNode.removeChild(existingButton);
        }
'''))
    if not elements:
        elements["input"] = dict(type="text",label="Input: ")
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
        element["id"] = f"{element['type']}_{_varnamefriendly(element['label'])}_{i+1}"
        element["name"] = name if "name" not in element else element["name"]
        if not (element.get("step") is None):
            element["step"] = str(element["step"])
    def getHTML(element):
      match element["type"]:
        case "text" | "password" | "email" | "url" | "number" | "date" | "time" | "datetime-local" | "month" | "week" | "color" | "search" | "file" :
            return f'''<label for="{element['id']}">{element["label"]}</label>
                        <input id="{element['id']}" type="{element['type']}" name="{element['name']}" value="{element.get('value', '')}" step="{element.get('step','')}" placeholder="{element.get('placeholder','')}" style = "min-width: {max(20,len(str(element.get('value', ''))))}ch; font-family: monospace" oninput="this.style.width = ((this.value.length>=20) ? (this.value.length) : 20)+'ch';"/>'''
        case "range":
            return f'''<label for="{element['id']}">{element["label"]}</label>
                        <input id="{element['id']}" type="range" name="{element['name']}"
                               value="{element.get('value', '')}" min="{element.get('min', 0)}" max="{element.get('max', 100)}" 
                               step="{element['step']}"
                               oninput="this.nextElementSibling.value = this.value">
                                <output>{element.get('value', '')}</output>'''
        case "select" | "radio" | "checkbox":
            optionsHTML = '\n'.join(
                f'<option value="{option.replace("<br>","")}" {"selected" if option.replace("<br>","") == element.get("selected",None) else ""}>{option}</option>' if element["type"] == "select" else
                f'''<input type="{element['type']}" id="{element['id']}_{_varnamefriendly(option)}" name="{element['name']}" value="{option.replace("<br>","")}" {"checked" if option.replace("<br>","") in element.get("checked",[]) else ""}>
                   <label for="{element['id']}_{_varnamefriendly(option)}">{option}</label>'''
                for option in element.get("options",[])
            )
            if element["type"] == "select":
                return f'''<label for="{element['id']}">{element["label"]}</label>
                            <select id="{element['id']}" name="{element['name']}">\n{optionsHTML}\n</select>'''
            return f'''<div {'style="display: flex;"' if element['label'][-4:]!='<br>' else ""}><label for="{element['id']}">{element["label"]}</label>\n<div>{optionsHTML}</div></div>'''
        case "textarea":
            return f'''<label for="{element['id']}" style="vertical-align: top;">{element["label"]}</label>
                        <textarea id="{element['id']}" 
                                  name="{element['name']}" 
                                  style="background-color: #383838; color: #ccc; opacity: 1; border-color: #ccc;" value="{element.get('value', '')}"  placeholder="{element.get('placeholder','')}" 
                                    >{element.get('value', '')}</textarea>'''
        case _:
            return "Unknown element type"

    for element in elements.values():
        display(HTML(getHTML(element)))
    btnstyle = '"background-color: #444; color: #ccc; opacity: 1; border: 1px solid #444;"'
    display(HTML(f'''<button id="EnterBtn" style = {btnstyle}>Enter ↩️</button>\n'''))

    inputValuesJS = ""
    for element in elements.values():
        inputValuesJS += Javascript(f'''

    if ("{element["type"]}" === 'radio') {{
    var checkedradio = document.querySelector('input[name="{element["name"]}"]:checked');
    var returnValue = checkedradio ? checkedradio.value : "";
    //alert(checkedradioValue);

    var radios = document.querySelectorAll('input[name="{element["name"]}"]');

    // Loop through each radio button and disable it
    radios.forEach(radio => {{
        if (radio.type === "radio"){{
            radio.disabled = true;

            var label = document.querySelector(`label[for="${{radio.id}}"]`);
            if (label) {{
                if (radio != checkedradio) {{
                    label.style.color = "#777";
                }}
            }}
            radio.removeAttribute('id');
            radio.removeAttribute('name');
        }}
    }});
    }} else if ("{element["type"]}" === 'checkbox') {{
        var checkedboxes = document.querySelectorAll('input[name="{element["name"]}"]:checked');
        var returnValue = Array.from(checkedboxes).map(checkbox => checkbox.value);
        //alert(returnValue);

        // Loop through each checkbox and disable it
        var checkboxes = document.querySelectorAll('input[name="{element["name"]}"]');
        var checkboxesArray = Array.from(checkboxes);
        var uncheckedboxes = checkboxesArray.filter(checkbox => !checkbox.checked);
        // alert(uncheckedboxes);
        uncheckedboxes.forEach(checkbox => {{
            if (checkbox.type === "checkbox"){{
                var label = document.querySelector(`label[for="${{checkbox.id}}"]`);
                if (label) {{
                    label.style.color = "#777";
                }}
            }}
        }});
        checkboxes.forEach(checkbox => {{
            if (checkbox.type === "checkbox"){{
                checkbox.disabled = true;
                checkbox.removeAttribute('id');
                checkbox.removeAttribute('name');
            }}
        }});
    }} else {{
    var {element["id"]} = document.getElementById("{element["id"]}");
    {element["id"]}.disabled = true; {element["id"]}.style.cssText += style;
    var returnValue = {element["id"]}.value ? {element["id"]}.value : "";

    {element["id"]}.removeAttribute('id');
    {element["id"]}.removeAttribute('name');
    //alert(returnValue);
    }}

    inputValues.push(returnValue);
    ''').data

    return eval_js('''
new Promise((resolve) => {
  document.getElementById("EnterBtn").onclick = function() {
            var event = new KeyboardEvent('keydown', {
                key: 'Enter',
                keyCode: 13,
                code: 'Enter',
                which: 13,
                bubbles: true,
                cancelable: true
            });
            document.dispatchEvent(event);
        };
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();  // Prevent the default Enter key behavior
      // Check if a button with id "EnterBtn" already exists
      var existingButton = document.getElementById("EnterBtn");
      if (existingButton) {
            // Remove the existing button
            existingButton.parentNode.removeChild(existingButton);
      }

      var inputValues = [];
      var style="background-color: #383838; color: #ccc; opacity: 1; border-color: #383838;"
      '''+inputValuesJS+'''
      resolve(inputValues.length === 1 ? inputValues[0] : inputValues);
    }
  });
})
''')
    
def _coinputsingle(**element):
    name = "input_"+_varnamefriendly(str(element))[:50]+"_"+_varnamefriendly(str(time.time()))
    #print(name)
    return coinput(**{name:element})

def inputradio(label="Pick an Option: ", options=["Option A", "Option B", "Option C"], **kwargs):
    if isinstance(label, list|tuple):
        options = label
        label = "Select your options:"
    return _coinputsingle(
        label=label,
        type="radio",
        options=options,
        **kwargs
    )

def inputselect(label="Select an Option: ", options=["Option A", "Option B", "Option C"], **kwargs):
    if isinstance(label, list|tuple):
        options = label
        label = "Select an Option:"
    return _coinputsingle(
        label=label,
        type="select",
        options=options,
        **kwargs
    )

def inputcheckbox(label="Select your options: ", options=["Option A", "Option B", "Option C"], **kwargs):
    if isinstance(label, list|tuple):
        options = label
        label = "Select your options:"
    return _coinputsingle(
        label=label,
        type="checkbox",
        options=options,
        **kwargs
    )

def inputtext(label="Enter Text: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="text",
        **kwargs
    )

def inputnumber(label="Enter a Number: ", step=1, **kwargs):
    return _coinputsingle(
        label=label,
        type="number",
        step=step,
        **kwargs
    )

def inputrange(label="Select a Value: ", min=0, max=100, step=1, **kwargs):
    return _coinputsingle(
        label=label,
        type="range",
        min=min,
        max=max,
        step=step,
        **kwargs
    )

def inputtextarea(label="Enter Text: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="textarea",
        **kwargs
    )

def inputfile(label="Upload a File: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="file",
        **kwargs
    )

def inputdate(label="Select a Date: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="date",
        **kwargs
    )

def inputtime(label="Select a Time: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="time",
        **kwargs
    )

def inputdatetime(label="Select a Date and Time: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="datetime-local",
        **kwargs
    )

def inputmonth(label="Select a Month: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="month",
        **kwargs
    )

def inputweek(label="Select a Week: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="week",
        **kwargs
    )

def inputcolor(label="Select a Color: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="color",
        **kwargs
    )


def inputhidden(label="Hidden Input: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="hidden",
        **kwargs
    )

def inputpassword(label="Enter Password: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="password",
        **kwargs
    )

def inputurl(label="Enter a URL: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="url",
        **kwargs
    )


def inputcolor(label="Select a Color: ", **kwargs):
    return _coinputsingle(
        label=label,
        type="color",
        **kwargs
    )
