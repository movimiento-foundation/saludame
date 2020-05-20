Updates messages:
1. Update POTFILES.in
2. Delete the folder locale
3. In the activity root, execute: python setup.py
   This generates a new Saludame.pot
4. Move to the po folder
5. msgmerge es.po Saludame.pot
   Don't close it, here you can see the sintax highlited
6. msgmerge es.po Saludame.pot -o es.po
   Now the files are merged, use the terminal output to fix the file if neccesary.
7. mkdir -p ../locale/es/LC_MESSAGES/
8. Compile:
   msgfmt -o ../locale/es/LC_MESSAGES/org.ceibaljam.Saludame.mo es.po
