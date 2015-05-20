using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Excel = Microsoft.Office.Interop.Excel;
using Office = Microsoft.Office.Core;
using Microsoft.Office.Tools.Excel;
using ZMQ = ZeroMQ;

namespace addin
{
    public partial class ThisAddIn
    {
        private ZMQ.ZContext ctx;
        private ZMQ.ZSocket client;

        private void InitZmqClient() 
        {
            ctx = new ZMQ.ZContext();
            client = new ZMQ.ZSocket(ctx, ZMQ.ZSocketType.REQ);
            client.Connect("tcp://127.0.0.1:8080");
        }

        private void DestroyZmqClient() 
        {
            client.Close();
            ctx.Shutdown();
        }

        private String SendEvent(object sender, System.EventArgs e) 
        {
            return SendEvent(sender.ToString() + e.ToString());
        }

        private String SendEvent(String msg)
        {
            client.Send(new ZMQ.ZFrame(msg));
            using (ZMQ.ZFrame reply = client.ReceiveFrame())
            {
                return reply.ReadString();
            }
        }

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            InitZmqClient();
            SendEvent(sender, e);
            this.Application.WorkbookOpen += new Excel.AppEvents_WorkbookOpenEventHandler(ThisAddIn_WorkbookOpen);
        }

        void ThisAddIn_CellsChange(Excel.Range target)
        {
            SendEvent("Change: " + target.Cells.Count);
        }

        void ThisAddIn_WorkbookOpen(Excel.Workbook Wb)
        {
            SendEvent("Open workbook: " + Wb.FullName);

            foreach (Excel.Worksheet ws in Wb.Worksheets)
            {
                SendEvent("Worksheet named " + ws.Name);
                ws.Change += ThisAddIn_CellsChange;
            }
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            SendEvent(sender, e);
            DestroyZmqClient();
        }

        #region Код, автоматически созданный VSTO

        /// <summary>
        /// Обязательный метод для поддержки конструктора - не изменяйте
        /// содержимое данного метода при помощи редактора кода.
        /// </summary>
        private void InternalStartup()
        {
            this.Startup += new System.EventHandler(ThisAddIn_Startup);
            this.Shutdown += new System.EventHandler(ThisAddIn_Shutdown);
        }
        
        #endregion
    }
}
