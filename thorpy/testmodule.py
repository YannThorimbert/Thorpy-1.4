def run():
    import thorpy
    application = thorpy.Application((600, 600), "ThorPy test")

    ##thorpy.theme.set_theme("human")

    #### SIMPLE ELEMENTS ####

    ghost = thorpy.Ghost()
    ghost.finish()

    element = thorpy.Element("Element")
    element.finish()
    thorpy.makeup.add_basic_help(element,
                               "Element instance:\nMost simple graphical element.")

    clickable = thorpy.Clickable("Clickable")
    clickable.finish()
    clickable.add_basic_help("Clickable instance:\nCan be hovered and pressed.")

    draggable = thorpy.Draggable("Draggable")
    draggable.finish()
    thorpy.makeup.add_basic_help(draggable, "Draggable instance:\nYou can drag it.")

    #### SIMPLE Setters ####

    checker_check = thorpy.Checker("Checker")
    checker_check.finish()
    thorpy.makeup.add_basic_help(checker_check,
                               "Checker instance:\nHere it is of type 'checkbox'.")

    checker_radio = thorpy.Checker("Radio", typ="radio")
    checker_radio.finish()
    thorpy.makeup.add_basic_help(checker_radio,
                               "Checker instance:\nHere it is of type 'radio'.")

    browser = thorpy.Browser("../../", text="Browser")
    browser.finish()
    browser.set_prison()

    browserlauncher = thorpy.BrowserLauncher(browser, name_txt="Browser",
                                           file_txt="Nothing selected",
                                           launcher_txt="...")
    browserlauncher.finish()
    browserlauncher.scale_to_title()
    thorpy.makeup.add_basic_help(browserlauncher,
                               "Browser instance:\nA way for user to find a file or"
                               +"\na folder on the computer.")

    dropdownlist = thorpy.DropDownListLauncher(name_txt="DropDownListLauncher",
                                             file_txt="Nothing selected",
                                             titles=[str(i) for i in range(1, 9)])
    dropdownlist.finish()
    dropdownlist.scale_to_title()
    thorpy.makeup.add_basic_help(dropdownlist,
                               "DropDownList:\nDisplay a list of choices.")

    slider = thorpy.SliderX(120, (5, 12), "Slider: ", typ=float, initial_value=8.4)
    slider.finish()
    thorpy.makeup.add_basic_help(slider, "SliderX:\nA way for user to select a value."
                               +"\nCan select any type of number (int, float, ..).")
    slider.set_center

    inserter = thorpy.Inserter(name="Inserter: ", value="Write here.")
    inserter.finish()
    thorpy.makeup.add_basic_help(inserter,
                               "Inserter:\nA way for user to insert a value.")


    text_title = thorpy.make_text("Test Example", 25, (0,0,255))

    central_box = thorpy.Box("", [ghost, element, clickable, draggable, checker_check,
                                checker_radio, dropdownlist, browserlauncher,
                                slider, inserter])
    central_box.finish()
    central_box.center()
    central_box.add_lift()
    central_box.set_main_color((200,200,255,120))

    background = thorpy.Background(color=(200,200,200),
                                 elements=[text_title, central_box])
    background.finish()

    thorpy.store(background)

    menu = thorpy.Menu(background)
    menu.play()

    application.quit()



if __name__ == "__main__":
    run()
