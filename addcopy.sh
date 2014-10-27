#!/bin/bash

gpl=$(< gpl_declaration.py)
for f in `git ls-files '*.py'`
do
    case "$(< $f)" in
	*$gpl*)			# Do nothing
	    ;;
	'#!'*)			# Preserve the sh-bang line
	    { 
		head -n 1 $f; 
		echo; 
		cat gpl_declaration.py;
		tail -n +2 $f;
	    } > $f-t
	    mv -f $f-t $f 2> /dev/null
	    ;;
	*)			# Prepend the notice
	    cat gpl_declaration.py $f > $f-t
	    mv $f-t $f 2> /dev/null
	    ;;
    esac
done
