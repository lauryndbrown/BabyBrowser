<h1 align="center">
  <br>
  <img src="https://github.com/lauryndbrown/BabyBrowser/blob/master/baby_browser/assets/images/crib.png" alt="BabyBrowser" width="100">
  <br>
  BabyBrowser
  <br>
</h1>
<p align="center"><strong>A Small Web Browser Built in Python</strong></p>

![Demo Gif](https://github.com/lauryndbrown/BabyBrowser/blob/master/baby_browser/Screenshots/demo3.gif)

Check the [Examples folder](https://github.com/lauryndbrown/BabyBrowser/tree/master/baby_browser/Examples) for HTML pages the web browser can interpret.
# Install & Run
```shell
> pip install babybrowser
> babybrowser
```
# Features
## System Overview
- Networking
  - Get Retrival of websites and images
- Browser User Interface built in PyQT
  - Back and Forward Buttons
  - Webpage Bookmarking Feature
  - Multiple Movable/Closable Browser Tabs with Webpage Title Display
- Webpage Rendering
  - Html Interpreter to build a DOM
  - Base Browser CSS
  - Style Sheet Cascading
  - CSS calculated as-needed by the interpreter
  - Translation of the DOM to PyQT elements
## Implemented HTML 
  - Head Tags: Title, Style
  - Self Closing Tags: HR, IMG, BR
  - Additional In-Body Tags: P, H1-H6
## Implemented CSS
  - Font: Color, Size, Weight
  - BoxStyles: background-color
