# card-checkr

> Pokemon set symbol locator and itdentifier for use in card scanning systems

## About the Project

    Card-Checker is a python module that atempts to locate and identify set symbols on pokemon trading cards. This was originally created as a project to solve an issue in a card processing application. This module is intended for anyone who is creating card matching applications for trading cards, specificly in this case, pokemon cards.
    
## Built With
- [Python](https://www.python.org)
- [MacOS Vision](https://macos.readthedocs.io/en/stable/vision.html)

### Prerequisites
- [MacOS Vision](https://macos.readthedocs.io/en/stable/vision.html)
- [Quartz] (https://pypi.org/project/pyobjc-framework-Quartz/)
- [NSData] (https://developer.apple.com/documentation/foundation/nsdata)

## Usage
    Card-Checkr is works best on card scans from a Fujitsu 8170 as that is the machine that I used however any scan that has the card in the center of the image should work with it.

    1. Create a gallery of the set symbols you want to look for to do this create a call like
        gallery_pictures_example = Path(Path/to/Images)
        gallery_example = build_gallery.build_gallery(gallery_pictures_example)
    2. Create an instance of the CardChecker class.
    3. Call the get_card_set method using the image directory of the card and the gallary. 


## License
    Feel free to use in any projects you want and change this in any way you see fit!

## Contact
**Caden Sak**

- GitHub: [@CadenSak](https://github.com/CadenSak)
- Email: sakcaden@gmail.com
- Project Link: https://github.com/CadenSak/card-checkr

## Acknowledgments
- [MacOS Vision](https://macos.readthedocs.io/en/stable/vision.html)
- Everyone who contributed to this project
