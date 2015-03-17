using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Excel = Microsoft.Office.Interop.Excel;
using Office = Microsoft.Office.Core;
using Microsoft.Office.Tools.Excel;
using System.Web;
using System.Net.Http;

namespace addin
{
    class Range
    {
        Excel.Range range;

        public Range(Excel.Range range)
        {
            this.range = range;
        }

        private static String Serialize(Excel.Range range)
        {
            String result = "";
            foreach(Excel.Range cell in range.Cells) 
            {
                String value = ((String)cell.Text).Trim();
                if ((value != null) && (value != "")) 
                {
                    result += cell.Address + "=" + System.Net.WebUtility.UrlEncode(value);
                }
            }
            return null;
        }
    }
}
