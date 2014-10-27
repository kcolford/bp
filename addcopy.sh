#!/bin/bash

gpl=$(< gpl_declaration.py)
for f in `git ls-files '*.py'`
do
    case "$(< $f)" in
	*$gpl*)			# GPL already there, do nothing
	    ;;
	'#!'*)			# Preserve the sh-bang line
	    { 
		head -n 1 $f; 
		echo; 
		cat gpl_declaration.py;
		tail -n +2 $f;
	    } > $f-t
	    ;;
	*)			# Prepend the notice
	    cat gpl_declaration.py $f > $f-t
	    ;;
    esac

    # Replace old file with new file.
    if [ -f $f-t ]; then
	chmod --reference=$f $f-t # preserve mode bits
	mv $f-t $f
    fi
done
