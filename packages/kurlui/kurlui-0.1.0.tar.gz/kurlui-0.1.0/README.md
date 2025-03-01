# KurlUI

KurlUI is a Python UI library inspired by the Roblox Rayfield library, built with Tkinter.

## Installation

```sh
pip install kurlui
```

## Usage

```python
from kurlui import KurlUI 

def on_button_click():
    print("Button Clicked!")

ui = RayfieldUI()
tab = ui.create_tab("Main")
ui.add_button(tab, "Click Me", on_button_click)
ui.run()
```