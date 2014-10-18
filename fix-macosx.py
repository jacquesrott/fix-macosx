#!/usr/bin/python

import os
import sys

from Foundation import (
    CFPreferencesSynchronize, CFPreferencesCopyValue, CFPreferencesCopyKeyList,
    CFPreferencesSetValue, CFPreferencesCopyMultiple, CFPreferencesSetMultiple,
    kCFPreferencesCurrentUser, kCFPreferencesAnyHost, NSMutableArray,
    NSMutableDictionary)


DISABLED_ITEMS = set(["MENU_WEBSEARCH", "MENU_SPOTLIGHT_SUGGESTIONS"])
REQUIRED_ITEM_KEYS = set(["enabled", "name"])

BUNDLE_ID = "com.apple.Spotlight"
PREF_NAME = "orderedItems"

DEFAULT_VALUES = [
    {'enabled' : True, 'name' : 'APPLICATIONS'},
    {'enabled' : True, 'name' : 'MENU_CONVERSION'},
    {'enabled' : True, 'name' : 'MENU_EXPRESSION'},
    {'enabled' : True, 'name' : 'MENU_DEFINITION'},
    {'enabled' : True, 'name' : 'SYSTEM_PREFS'},
    {'enabled' : True, 'name' : 'DOCUMENTS'},
    {'enabled' : True, 'name' : 'DIRECTORIES'},
    {'enabled' : True, 'name' : 'PRESENTATIONS'},
    {'enabled' : True, 'name' : 'SPREADSHEETS'},
    {'enabled' : True, 'name' : 'PDF'},
    {'enabled' : True, 'name' : 'MESSAGES'},
    {'enabled' : True, 'name' : 'CONTACT'},
    {'enabled' : True, 'name' : 'EVENT_TODO'},
    {'enabled' : True, 'name' : 'IMAGES'},
    {'enabled' : True, 'name' : 'BOOKMARKS'},
    {'enabled' : True, 'name' : 'MUSIC'},
    {'enabled' : True, 'name' : 'MOVIES'},
    {'enabled' : True, 'name' : 'FONTS'},
    {'enabled' : True, 'name' : 'MENU_OTHER'},
    {'enabled' : False, 'name' : 'MENU_SPOTLIGHT_SUGGESTIONS'},
    {'enabled' : False, 'name' : 'MENU_WEBSEARCH'},
]


def main():
    # OS X Yosemite's Spotlight is only supported
    major_release = int(os.uname()[2].split(".")[0])
    if major_release < 14:
      print "Good news! This version of Mac OS X's Spotlight is not known to invade your privacy."
      sys.exit(0)

    fix_spotlight()
    print "All done. Make sure to log out (and back in) for the changes to take effect."


def fix_spotlight():
    items = CFPreferencesCopyValue(
        PREF_NAME, BUNDLE_ID,
        kCFPreferencesCurrentUser, kCFPreferencesAnyHost)

    # Actual preference values are populated on demand; if the user
    # hasn't previously configured Spotlight, the preference value
    # will be unavailable
    new_items = DEFAULT_VALUES
    if items:
        new_items = NSMutableArray.new()
        for item in items:
            missing_keys = [key for key in REQUIRED_ITEM_KEYS if not key in item]

            if missing_keys:
                print "Preference item %s is missing expected keys (%s), skipping" % (item, missing_keys)
                new_items.append(item)
                continue

            if not item["name"] in DISABLED_ITEMS:
                new_items.append(item)
                continue

        new_item = NSMutableDictionary.dictionaryWithDictionary_(item)
        new_item.setObject_forKey_(0, "enabled")
        new_items.append(new_item)

    CFPreferencesSetValue(PREF_NAME, new_items, BUNDLE_ID, kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
    CFPreferencesSynchronize(BUNDLE_ID, kCFPreferencesCurrentUser, kCFPreferencesAnyHost)


if __name__ == "__main__":
    main()
