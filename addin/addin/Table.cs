using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Excel = Microsoft.Office.Interop.Excel;
using Office = Microsoft.Office.Core;
using Microsoft.Office.Tools.Excel;

namespace addin
{
    class Table
    {
        Excel.ListObject table;

        public Table(Excel.ListObject table) 
        {
            this.table = table;
        }
    }
}
