for img in *.png; do
    fixed=`echo $img | tr " " "_"`
    sed -E -i "s/$img/$fixed/g" *.md
    mv "$img" $fixed
done
