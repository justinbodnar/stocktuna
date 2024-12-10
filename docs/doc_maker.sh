# create pydoc3 html files
for file in stocktuna/*.py; do
    modname=$(basename "$file" .py)
    python3 -m pydoc -w "stocktuna.$modname"
done
# remove all broken links
find . -name "*.html" -print0 | while IFS= read -r -d '' file; do
    # Extract all potential HTML links
    grep -o 'href="[^"]*.html"' "$file" | sed 's/href="//;s/"$//' | while read -r link; do
        # Check if the link target exists
        if [ ! -f "$link" ]; then
            # Link target doesn't exist, remove the hyperlink in the HTML file
            sed -i "s|<a href=\"$link\">[^<]*</a>|$(basename "$link" .html)|g" "$file"
        fi
    done
done

# add opening php code
echo "<?php require \"header.php\"; ?>" > stocktuna.stocktuna.php
echo "<?php require \"header.php\"; ?>" > stocktuna.cannedtuna.php

# add main contanet
cat stocktuna.stocktuna.html >> stocktuna.stocktuna.php
cat stocktuna.cannedtuna.html >> stocktuna.cannedtuna.php

# add closing php code
echo "<?php require \"footer.php\"; ?>" >> stocktuna.stocktuna.php
echo "<?php require \"footer.php\"; ?>" >> stocktuna.cannedtuna.php

# edit specific tags
sed -i 's/<font color="#ffffff">/<font color="#000000">/g' stocktuna.stocktuna.php
sed -i 's/<font color="#ffffff">/<font color="#000000">/g' stocktuna.cannedtuna.php

# change stocktuna.stocktuna.html filename extension
sed -i 's/stocktuna.stocktuna.html/stocktuna.stocktuna.php/g' stocktuna.stocktuna.php
sed -i 's/stocktuna.stocktuna.html/stocktuna.stocktuna.php/g' stocktuna.cannedtuna.php

# change stocktuna.cannedtuna.html filename extension
sed -i 's/stocktuna.cannedtuna.html/stocktuna.cannedtuna.php/g' stocktuna.stocktuna.php
sed -i 's/stocktuna.cannedtuna.html/stocktuna.cannedtuna.php/g' stocktuna.cannedtuna.php

# change hyperlink to stocktuna.html
sed -i 's/href="stocktuna.html/href="stocktuna.stocktuna.php/g' stocktuna.stocktuna.php
sed -i 's/href="stocktuna.html/href="stocktuna.stocktuna.php/g' stocktuna.cannedtuna.php

# remove dead hyperlink
sed -i 's-<a href="builtins.html#object">builtins.object</a>-builtins.object-g' stocktuna.stocktuna.php
sed -i 's-<a href="builtins.html#object">builtins.object</a>-builtins.object-g' stocktuna.cannedtuna.php

sed -i 's-<a href="builtins.html#object">object</a>-object-g' stocktuna.stocktuna.php
sed -i 's-<a href="builtins.html#object">object</a>-object-g' stocktuna.cannedtuna.php

sed -i 's-<a href="file:/root/stocktuna/stocktuna/stocktuna.py">/root/stocktuna/stocktuna/stocktuna.py</a>--g' stocktuna.stocktuna.php
sed -i 's-<a href="file:/root/stocktuna/stocktuna/cannedtuna.py">/root/stocktuna/stocktuna/cannedtuna.py</a>--g' stocktuna.cannedtuna.php

sed -i 's-<a href=".">index</a>-<a href=".">Home</a>-g' stocktuna.stocktuna.php
sed -i 's-<a href=".">index</a>-<a href=".">Home</a>-g' stocktuna.cannedtuna.php

# move files to webroot
mv stocktuna.stocktuna.php /var/www/html/stocktuna.com/stocktuna.stocktuna.php
mv stocktuna.cannedtuna.php /var/www/html/stocktuna.com/stocktuna.cannedtuna.php

# remove tmp files
rm stocktuna.stocktuna.*
rm stocktuna.cannedtuna.*
rm stocktuna.__init__.*
