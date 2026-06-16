echo "===== PATCHPILOT HEALTH CHECK ====="

echo ""
echo "Python:"
which python

echo ""
echo "GPU:"
python -c "import torch; print(torch.cuda.is_available())"

echo ""
echo "GPU Name:"
python -c "import torch; print(torch.cuda.get_device_name(0))"

echo ""
echo "Database:"
ls -lh patchpilot.db

echo ""
echo "Assets:"
python -c "
import pandas as pd
import sqlite3
conn=sqlite3.connect('patchpilot.db')
print(pd.read_sql('select count(*) as total from assets',conn))
"

echo ""
echo "Transformers:"
python -c "import transformers; print(transformers.__version__)"

echo ""
echo "DONE"
