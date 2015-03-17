VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Dim PrevValue As String
Dim MarkedAddress As String
Dim Updated As Boolean



Private Function GetColumnName(ByVal Column As Range) As String
    Dim WS As Worksheet
    Dim Result As String
    
    Set WS = ActiveWorkbook.ActiveSheet
    Result = Replace(Column.Address, "1", "")
    Result = Replace(Result, "2", "")
    Result = Replace(Result, "3", "")
    Result = Replace(Result, "4", "")
    Result = Replace(Result, "5", "")
    Result = Replace(Result, "6", "")
    Result = Replace(Result, "7", "")
    Result = Replace(Result, "8", "")
    Result = Replace(Result, "9", "")
    Result = Replace(Result, "0", "")
    Result = Replace(Result, "$", "")
    GetColumnName = WS.Name & "!" & Result
End Function

Private Function Serialize(ByVal Target As Range) As String
   Dim Result As String
    Result = "&column=" & GetColumnName(Target)
    For iRow = 1 To Target.Rows.Count
        For iCol = 1 To Target.Columns.Count
            If Trim(Target.Cells(iRow, iCol).Text & vbNullString) = vbNullString Then
            Else
                Result = Result & "&" & Target.Cells(iRow, iCol).Address & "=" & Target.Cells(iRow, iCol).Text
            End If
        Next iCol
    Next iRow
    Serialize = Result
End Function

Private Function SerializeCorrected(ByVal Target As Range, ByVal Corrected As String) As String
   Dim Result As String
    Result = "&column=" & GetColumnName(Target)
    For iRow = 1 To Target.Rows.Count
        For iCol = 1 To Target.Columns.Count
            If Trim(Target.Cells(iRow, iCol).Text & vbNullString) = vbNullString Then
            Else
                Result = Result & "&" & Target.Cells(iRow, iCol).Address & "=" & Corrected & "&" & Target.Cells(iRow, iCol).Address & "=" & Target.Cells(iRow, iCol).Text
            End If
        Next iCol
    Next iRow
    SerializeCorrected = Result
End Function

Private Function SerializeColumn(ByVal Target As Range, ByVal Index As Integer) As String
    Dim Result As String
    Dim SubResult As String
    Result = "&column=" & GetColumnName(Target.Cells(1, Index))
        For iRow = 1 To Target.Rows.Count
            If Trim(Target.Cells(iRow, Index).Text & vbNullString) = vbNullString Then
            Else
                SubResult = SubResult & "&" & Target.Cells(iRow, Index).Address & "=" & Target.Cells(iRow, Index).Text
            End If
    Next iRow
    If Trim(SubResult & vbNullString) = vbNullString Then
        SerializeColumn = ""
    Else
        SerializeColumn = Result & SubResult
    End If
End Function

Private Function PostTable(ByVal Target As Range) As String
   Dim QT As QueryTable
   Dim Dest As Range
   Dim Serialized As String
   Set Dest = ActiveSheet.Range("ZZ1")
   For iCol = 1 To Target.Columns.Count
       Serialized = SerializeColumn(Target, iCol)
       If Trim(Serialized & vbNullString) = vbNullString Then
       Else
           Set QT = ActiveSheet.QueryTables.Add(Connection:="URL;http://localhost:8000/analyzer", Destination:=Dest)
           With QT
               .PostText = "action=check_new" & Serialized
               .RefreshStyle = xlOverwriteCells
               .SaveData = True
               .Refresh False
            End With
            PostData = Dest.Value
            QT.Delete
        End If
    Next iCol
End Function

Private Function PostChange(ByVal Target As Range, ByVal Action As String) As String
   Dim QT As QueryTable
   Dim Dest As Range
   Set Dest = ActiveSheet.Range("ZZ2")
   Set QT = ActiveSheet.QueryTables.Add(Connection:="URL;http://localhost:8000/analyzer", Destination:=Dest)
   With QT
       .PostText = "action=" & Action & Serialize(Target)
       If Action = "cell_corrected" Then
           .PostText = "action=" & Action & SerializeCorrected(Target, PrevValue)
       End If
       .RefreshStyle = xlOverwriteCells
       .SaveData = True
       .Refresh False
   End With
   PostChange = Dest.Text
   QT.Delete
End Function

Public Sub PostUnmarked()
Attribute PostUnmarked.VB_ProcData.VB_Invoke_Func = "q\n14"
    Dim Cell As Range
    Dim Output As String
    If Trim(MarkedAddress & vbNullString) = vbNullString Then
    Else
        Set Cell = ActiveSheet.Range(MarkedAddress)
        Cell.Style = "Normal"
        Output = PostChange(Cell, "cell_unmarked")
    End If
End Sub


Public Sub ApplyOutput(ByVal Output As String)
    Dim Pairs() As String
    Dim Pair As String
    Dim AV() As String
    Dim Address As String
    Dim Value As String
    Dim Cell As Range
    
    Pairs() = Split(Output, "&")
    For i = LBound(Pairs) To UBound(Pairs)
        Pair = Pairs(i)
        AV() = Split(Output, "=")
        Address = Replace(AV(0), "$", "")
        Value = Trim(AV(1))
        Set Cell = ActiveSheet.Range(Address)
        If Value = "INCORRECT" Then
            'Cell.Style = "Bad"
            Cell.Interior.ColorIndex = 22
            MarkedAddress = Address
            Application.OnUndo "Undo Mark Incorrect", "!Sheet1.PostUnmarked"
        Else
            'Cell.Style = "Normal"
            Cell.Interior.ColorIndex = 0
        End If
    Next i

End Sub

Private Sub Worksheet_Activate()
    Dim WS As Worksheet
    Dim WB As Workbook
    Dim i As Long
    Dim Value As Range
    Dim Output As String
    
    Set WB = ActiveWorkbook
    Set WS = WB.ActiveSheet
    
    'For i = 1 To WS.QueryTables.Count
    '    WS.QueryTables.Item(i).Delete
    'Next i
    
    For i = 1 To WS.ListObjects.Count
        Set Value = WS.ListObjects.Item(i).DataBodyRange
        If Value.Cells.Address = "$ZZ$2" Or Value.Cells.Address = "$ZZ$1" Then
        Else
            Output = PostTable(Value)
        End If
    Next i
    
End Sub

Private Sub Worksheet_Change(ByVal Target As Range)
    Dim Output As String
    If Target.Cells.Count = 1 Then
        If Trim(Target.Value & vbNullString) = vbNullString Then
        Else
            If Trim(PrevValue & vbNullString) = vbNullString Then
                If Target.Cells.Address = "$ZZ$2" Or Target.Cells.Address = "$ZZ$1" Then
                Else
                    Output = PostChange(Target, "check_new")
                    ApplyOutput Output
                End If
            Else
                If PrevValue = Target.Value Then
                Else
                    If Target.Cells.Address = "$ZZ$2" Or Target.Cells.Address = "$ZZ$1" Then
                    Else
                        Output = PostChange(Target, "cell_corrected")
                        ApplyOutput Output
                    End If
                End If
            End If
        End If
    End If
End Sub

Public Sub Worksheet_SelectionChange(ByVal Target As Range)
    If Target.Cells.Address = "$ZZ$2" Or Target.Cells.Address = "$ZZ$1" Then
    Else
    If Target.Cells.Count = 1 Then
         PrevValue = Target.Value
    Else
         PrevValue = ""
    End If
    End If
End Sub
