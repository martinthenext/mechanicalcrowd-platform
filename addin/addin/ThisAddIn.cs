using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Excel = Microsoft.Office.Interop.Excel;
using Office = Microsoft.Office.Core;
using Microsoft.Office.Tools.Excel;
using ZeroMQ;
using System.Threading;

namespace addin
{
    class Router
    {
        private ZContext ctx;
        private String ident;
        private ZSocket subscriber;
        private ZSocket event_socket;
        private ZSocket async_socket;
        private Excel.Application excel;
        private CancellationTokenSource cancel;
        
        public Router(ZContext ctx, String ident, Excel.Application excel)
        {
            this.ctx = ctx;
            this.ident = ident;
            this.excel = excel;
            this.subscriber = new ZSocket(ctx, ZSocketType.SUB);
            this.event_socket = new ZSocket(ctx, ZSocketType.REQ);
            this.async_socket = new ZSocket(ctx, ZSocketType.REQ);
            this.cancel = new CancellationTokenSource();
        }

        private bool SubscriberHandler(ZSocket socket, out ZMessage message, out ZError error)
        {

            message = socket.ReceiveMessage();
            String payload = message[1].ReadString();
            this.event_socket.Send(new ZFrame(payload));
            error = default(ZError);
            return true;
        }

        private bool EventHandler(ZSocket socket, out ZMessage message, out ZError error)
        {
            message = socket.ReceiveMessage();
            error = null;
            return true;
        }

        private bool AsyncHandler(ZSocket socket, out ZMessage message, out ZError error)
        {
            message = socket.ReceiveMessage();
            String payload = message[0].ReadString();
            socket.Send(new ZFrame(socket.IdentityString));
            // do something with payload
            excel.ActiveSheet.Cells[1, 1] = "FUUUUUCK!";
            error = null;
            return true;
        }

        public void Run()
        {
            subscriber.Connect("inproc://events");
            subscriber.SetOption(ZSocketOption.SUBSCRIBE, "");

            event_socket.SetOption(ZSocketOption.IDENTITY, "event-" + ident);
            event_socket.Connect("tcp://127.0.0.1:8080");
            
            async_socket.SetOption(ZSocketOption.IDENTITY, "async-" + ident);
            async_socket.Connect("tcp://127.0.0.1:8080");
            

            ZError error = default(ZError);
            ZMessage[] messages = null;

            ZSocket[] sockets = new ZSocket[] { 
                subscriber, event_socket, async_socket };

            ZPollItem[] polls = new ZPollItem[] {
                ZPollItem.Create(SubscriberHandler), 
                ZPollItem.Create(EventHandler), 
                ZPollItem.Create(AsyncHandler)
            };

            async_socket.Send(new ZFrame(async_socket.IdentityString));

            try
            {
                while (!cancel.IsCancellationRequested)
                {
                    if (!sockets.Poll(polls, ZPoll.In, ref messages, out error, TimeSpan.FromMilliseconds(500)))
                    {
                        if (error == ZError.EAGAIN)
                        {
                            Thread.Sleep(1);
                            continue;
                        }

                        if (error == ZError.ETERM)
                        {
                            break;
                        }

                        throw new ZException(error);
                    }
                }
            }
            catch (ZException)
            {
                if (!cancel.IsCancellationRequested)
                {
                    throw;
                }
            }

            subscriber.Dispose();
            event_socket.Dispose();
            async_socket.Dispose();
        }

        public void Stop()
        {
            cancel.Cancel();
        }
    }

    public partial class ThisAddIn
    {
        private ZContext ctx;
        private ZSocket publisher;
        private Thread routerThread;
        private Router router;

        private void SendEvent(String msg)
        {
            using (ZMessage message = new ZMessage())
            {
                message.Add(new ZFrame("event"));
                message.Add(new ZFrame(msg));
                publisher.Send(message);
            }
        }

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            ctx = new ZContext();
            router = new Router(ctx, "im-am-ident", this.Application);
            routerThread = new Thread(router.Run);
            routerThread.Start();
            publisher = new ZSocket(ctx, ZSocketType.PUB);
            publisher.Bind("inproc://events");
            this.Application.WorkbookOpen += new Excel.AppEvents_WorkbookOpenEventHandler(ThisAddIn_WorkbookOpen);
            this.Application.SheetChange += new Excel.AppEvents_SheetChangeEventHandler(ThisAddIn_SheetChange);
            this.Application.WorkbookBeforeClose += new Excel.AppEvents_WorkbookBeforeCloseEventHandler(ThisAddIn_BeforeClose);
        }

        private void ThisAddIn_BeforeClose(Excel.Workbook wb, ref bool result)
        {
            router.Stop();
        }

        private void ThisAddIn_SheetChange(object Sh, Excel.Range Target)
        {
            SendEvent("Worksheet change: " + (Sh as Excel.Worksheet).Name + "; Value: " + Target.Value2);
        }

        void ThisAddIn_WorkbookOpen(Excel.Workbook Wb)
        {
            SendEvent("Open workbook: " + Wb.FullName);
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            routerThread.Join();
            publisher.Dispose();
            ctx.Dispose();
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
