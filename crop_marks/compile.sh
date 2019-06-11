for i in input/*
do
    if test -f "$i" 
    then
        cp $i input.pdf
        xelatex -synctex=1 -interaction=nonstopmode "crop_marks".tex
	xelatex -synctex=1 -interaction=nonstopmode "crop_marks".tex
	cp crop_marks.pdf $i 
    fi
done
