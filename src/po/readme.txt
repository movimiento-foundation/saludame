Requirements:
 - apt-get install gettext


Updates messages:
1. Update POTFILES.in
2. Delete the folder locale
3. Delete src/po/Saludame.pot
4. In the src/ dir run: xgettext --language=python --files-from=po/POTFILES.in --output=po/Saludame.pot
5. msgmerge po/es.po po/Saludame.pot
   Don't close it, here you can see the sintax highlited
6. msgmerge po/es.po po/Saludame.pot -o po/es.po
   Now the files are merged, use the terminal output to fix the file if neccesary.
7. mkdir -p ../locale/es/LC_MESSAGES/
8. Compile:
   msgfmt -o locale/es/LC_MESSAGES/org.ceibaljam.Saludame.mo po/es.po
