# MQL5 Syntax Reference for VS Code Themes

This document categorizes MQL5 syntax elements for consistent color theme application.

---

## Preprocessor Directives
```
#property  #include  #define  #import  #resource
```

## Data Types
```
int  double  string  bool  datetime  color  ulong  long  float  short  char  void  uint  uchar  ushort group
```

## Control Flow Keywords
```
if  else  for  while  do  switch  case  default  break  continue  return  goto
```

## Storage Modifiers
```
input  extern  static  const  virtual  override  private  protected  public  class  struct  enum
```

---

## Trade Functions
```
OrderSend  OrderSendAsync  OrderCalcMargin  OrderCalcProfit  OrderCheck
PositionSelect  PositionSelectByTicket  PositionGetSymbol  PositionGetTicket
PositionsTotal  OrdersTotal  HistorySelect  HistoryOrderSelect  HistoryDealSelect
```

## CTrade Class Methods
```
Buy  Sell  BuyLimit  BuyStop  SellLimit  SellStop
PositionOpen  PositionClose  PositionClosePartial  PositionCloseBy  PositionModify
OrderOpen  OrderModify  OrderDelete
SetExpertMagicNumber  SetDeviationInPoints  SetTypeFilling  SetAsyncMode
```

## Trade Request Actions (ENUM_TRADE_REQUEST_ACTIONS)
```
TRADE_ACTION_DEAL  TRADE_ACTION_PENDING  TRADE_ACTION_SLTP
TRADE_ACTION_MODIFY  TRADE_ACTION_REMOVE  TRADE_ACTION_CLOSE_BY
```

---

## Order Type Constants (ENUM_ORDER_TYPE)
```
ORDER_TYPE_BUY  ORDER_TYPE_SELL
ORDER_TYPE_BUY_LIMIT  ORDER_TYPE_SELL_LIMIT
ORDER_TYPE_BUY_STOP  ORDER_TYPE_SELL_STOP
ORDER_TYPE_BUY_STOP_LIMIT  ORDER_TYPE_SELL_STOP_LIMIT
ORDER_TYPE_CLOSE_BY
```

## Order State Constants (ENUM_ORDER_STATE)
```
ORDER_STATE_STARTED  ORDER_STATE_PLACED  ORDER_STATE_CANCELED
ORDER_STATE_PARTIAL  ORDER_STATE_FILLED  ORDER_STATE_REJECTED
ORDER_STATE_EXPIRED  ORDER_STATE_REQUEST_ADD  ORDER_STATE_REQUEST_MODIFY
ORDER_STATE_REQUEST_CANCEL
```

## Order Filling Modes (ENUM_ORDER_TYPE_FILLING)
```
ORDER_FILLING_FOK  ORDER_FILLING_IOC  ORDER_FILLING_RETURN  ORDER_FILLING_BOC
```

## Order Time Types (ENUM_ORDER_TYPE_TIME)
```
ORDER_TIME_GTC  ORDER_TIME_DAY  ORDER_TIME_SPECIFIED  ORDER_TIME_SPECIFIED_DAY
```

---

## Position Constants (ENUM_POSITION_TYPE)
```
POSITION_TYPE_BUY  POSITION_TYPE_SELL
```

## Position Properties (ENUM_POSITION_PROPERTY_INTEGER/DOUBLE/STRING)
```
POSITION_TICKET  POSITION_TIME  POSITION_TIME_MSC  POSITION_TIME_UPDATE
POSITION_TYPE  POSITION_MAGIC  POSITION_IDENTIFIER  POSITION_REASON
POSITION_VOLUME  POSITION_PRICE_OPEN  POSITION_PRICE_CURRENT
POSITION_SL  POSITION_TP  POSITION_SWAP  POSITION_PROFIT
POSITION_SYMBOL  POSITION_COMMENT  POSITION_EXTERNAL_ID
```

---

## Symbol ENUM Constants (ENUM_SYMBOL_INFO_...)
```
SYMBOL_EXIST  SYMBOL_DIGITS  SYMBOL_SPREAD  SYMBOL_TRADE_MODE
SYMBOL_TRADE_CALC_MODE  SYMBOL_TRADE_TICK_SIZE  SYMBOL_TRADE_TICK_VALUE
SYMBOL_VOLUME_MIN  SYMBOL_VOLUME_MAX  SYMBOL_VOLUME_STEP
SYMBOL_SWAP_LONG  SYMBOL_SWAP_SHORT  SYMBOL_MARGIN_INITIAL
SYMBOL_BID  SYMBOL_ASK  SYMBOL_POINT  SYMBOL_TRADE_STOPS_LEVEL
```

## Symbol Trade Modes (ENUM_SYMBOL_TRADE_MODE)
```
SYMBOL_TRADE_MODE_DISABLED  SYMBOL_TRADE_MODE_LONGONLY  SYMBOL_TRADE_MODE_SHORTONLY
SYMBOL_TRADE_MODE_CLOSEONLY  SYMBOL_TRADE_MODE_FULL
```

## Symbol Filling Modes (ENUM_SYMBOL_FILLING_MODE)
```
SYMBOL_FILLING_FOK  SYMBOL_FILLING_IOC
```

---

## Account ENUM Constants (ENUM_ACCOUNT_INFO_...)
```
ACCOUNT_LOGIN  ACCOUNT_TRADE_MODE  ACCOUNT_LEVERAGE  ACCOUNT_LIMIT_ORDERS
ACCOUNT_MARGIN_SO_MODE  ACCOUNT_TRADE_ALLOWED  ACCOUNT_TRADE_EXPERT
ACCOUNT_BALANCE  ACCOUNT_CREDIT  ACCOUNT_PROFIT  ACCOUNT_EQUITY
ACCOUNT_MARGIN  ACCOUNT_MARGIN_FREE  ACCOUNT_MARGIN_LEVEL
ACCOUNT_MARGIN_SO_CALL  ACCOUNT_MARGIN_SO_SO
ACCOUNT_CURRENCY  ACCOUNT_COMPANY  ACCOUNT_NAME  ACCOUNT_SERVER
```

## Account Trade Modes (ENUM_ACCOUNT_TRADE_MODE)
```
ACCOUNT_TRADE_MODE_DEMO  ACCOUNT_TRADE_MODE_CONTEST  ACCOUNT_TRADE_MODE_REAL
```

## Account Stop Out Modes (ENUM_ACCOUNT_STOPOUT_MODE)
```
ACCOUNT_STOPOUT_MODE_PERCENT  ACCOUNT_STOPOUT_MODE_MONEY
```

---

## Deal Constants (ENUM_DEAL_...)
```
DEAL_TYPE_BUY  DEAL_TYPE_SELL  DEAL_TYPE_BALANCE  DEAL_TYPE_CREDIT
DEAL_TYPE_CHARGE  DEAL_TYPE_CORRECTION  DEAL_TYPE_BONUS
DEAL_TYPE_COMMISSION  DEAL_TYPE_COMMISSION_DAILY
DEAL_ENTRY_IN  DEAL_ENTRY_OUT  DEAL_ENTRY_INOUT  DEAL_ENTRY_OUT_BY
DEAL_TICKET  DEAL_ORDER  DEAL_TIME  DEAL_TYPE  DEAL_ENTRY
DEAL_MAGIC  DEAL_REASON  DEAL_COMMISSION  DEAL_SWAP  DEAL_PROFIT
DEAL_VOLUME  DEAL_PRICE  DEAL_SYMBOL  DEAL_COMMENT
```

---

## Timeseries Functions
```
iTime  iOpen  iHigh  iLow  iClose  iVolume  iSpread
iTickVolume  iRealVolume  iBars  iBarShift  iHighest  iLowest
CopyRates  CopyTime  CopyOpen  CopyHigh  CopyLow  CopyClose
CopyTickVolume  CopyRealVolume  CopySpread  CopyTicks  CopySeries
```

## Timeframe Constants (ENUM_TIMEFRAMES)
```
PERIOD_CURRENT  PERIOD_M1  PERIOD_M2  PERIOD_M3  PERIOD_M4  PERIOD_M5
PERIOD_M6  PERIOD_M10  PERIOD_M12  PERIOD_M15  PERIOD_M20  PERIOD_M30
PERIOD_H1  PERIOD_H2  PERIOD_H3  PERIOD_H4  PERIOD_H6  PERIOD_H8  PERIOD_H12
PERIOD_D1  PERIOD_W1  PERIOD_MN1
```

---

## Symbol/Market Info Functions
```
SymbolInfoDouble  SymbolInfoInteger  SymbolInfoString  SymbolInfoTick
SymbolInfoSessionQuote  SymbolInfoSessionTrade
SymbolName  SymbolSelect  SymbolsTotal  SymbolExist
MarketBookAdd  MarketBookRelease  MarketBookGet
```

## Account Info Functions
```
AccountInfoDouble  AccountInfoInteger  AccountInfoString
```

---

## Common Functions
```
Print  PrintFormat  Alert  Comment  SendNotification  SendMail  SendFTP
Sleep  GetTickCount  GetMicrosecondCount
MessageBox  PlaySound  ExpertRemove  TerminalClose
```

## Conversion Functions
```
CharToString  StringToCharArray  TimeToString  StringToTime
DoubleToString  IntegerToString  NormalizeDouble  StringToDouble
ColorToString  StringToColor  EnumToString
```

## String Functions
```
StringLen  StringFind  StringSubstr  StringReplace
StringTrimLeft  StringTrimRight  StringSplit  StringConcatenate
StringFormat  StringCompare  StringToLower  StringToUpper
```

## Array Functions
```
ArraySize  ArrayResize  ArrayInitialize  ArrayFree  ArrayCopy
ArraySort  ArrayMaximum  ArrayMinimum  ArrayBsearch
ArraySetAsSeries  ArrayIsSeries  ArrayIsDynamic
```

## Math Functions
```
MathAbs  MathCeil  MathFloor  MathRound  MathPow  MathSqrt
MathLog  MathLog10  MathExp  MathMod  MathMax  MathMin
MathSin  MathCos  MathTan  MathArcsin  MathArccos  MathArctan
MathRand  MathSrand  MathIsValidNumber
```

## File Functions
```
FileOpen  FileClose  FileDelete  FileFlush  FileSeek  FileTell
FileRead  FileWrite  FileReadArray  FileWriteArray
FileReadDouble  FileReadInteger  FileReadString
FileWriteDouble  FileWriteInteger  FileWriteString
FileIsExist  FileCopy  FileMove  FileSize
```

---

## MQL5 Structures
```
MqlRates  MqlTick  MqlDateTime  MqlBookInfo
MqlTradeRequest  MqlTradeCheckResult  MqlTradeResult  MqlTradeTransaction
MqlParam  MqlSymbolInfo
```

## Standard Library Classes
```
CTrade  CPositionInfo  COrderInfo  CDealInfo  CHistoryOrderInfo
CSymbolInfo  CAccountInfo  CTerminalInfo  CExpertBase
CArray  CArrayObj  CArrayInt  CArrayDouble  CArrayString
CObject  CList  CHashMap  CDictionary
CIndicators  CIndicatorBuffer
CChartObject  CChartObjectText  CChartObjectLine  CChartObjectTrend
```

---

## Magic/Predefined Variables
```
_Symbol  _Digits  _Point  _Period  _LastError  _StopFlag
_UninitReason  _RandomSeed  _IsX64
Ask  Bid  Bars  Volume  Time  Open  High  Low  Close
```

## Event Handler Functions
```
OnInit  OnDeinit  OnStart  OnTick  OnTimer  OnTrade
OnTradeTransaction  OnBookEvent  OnChartEvent  OnCalculate
OnTester  OnTesterInit  OnTesterDeinit  OnTesterPass
```

## Return Codes (ENUM_INIT_RETCODE)
```
INIT_SUCCEEDED  INIT_FAILED  INIT_PARAMETERS_INCORRECT
INIT_AGENT_NOT_SUITABLE
```

---

## Terminal/Environment Constants
```
TERMINAL_CONNECTED  TERMINAL_TRADE_ALLOWED  TERMINAL_DLLS_ALLOWED
TERMINAL_EMAIL_ENABLED  TERMINAL_FTP_ENABLED  TERMINAL_NOTIFICATIONS_ENABLED
TERMINAL_MAXBARS  TERMINAL_CODEPAGE  TERMINAL_LANGUAGE
TERMINAL_COMPANY  TERMINAL_NAME  TERMINAL_PATH  TERMINAL_DATA_PATH
```

## Object Property Constants (OBJPROP_...)
```
OBJPROP_COLOR  OBJPROP_STYLE  OBJPROP_WIDTH  OBJPROP_BACK
OBJPROP_RAY_LEFT  OBJPROP_RAY_RIGHT  OBJPROP_SELECTABLE  OBJPROP_SELECTED
OBJPROP_TIME  OBJPROP_PRICE  OBJPROP_ANCHOR  OBJPROP_TEXT
OBJPROP_FONTSIZE  OBJPROP_CORNER  OBJPROP_XDISTANCE  OBJPROP_YDISTANCE
```

---

## Boolean Constants
```
true  false
```

## Numeric Limits
```
DBL_MAX  DBL_MIN  DBL_EPSILON  INT_MAX  INT_MIN
ULONG_MAX  LONG_MAX  LONG_MIN  EMPTY_VALUE  EMPTY  CLR_NONE  WRONG_VALUE
NULL  CHARTS_MAX  WHOLE_ARRAY
```

## Color Constants
```
clrRed  clrGreen  clrBlue  clrYellow  clrWhite  clrBlack
clrGray  clrSilver  clrOrange  clrPurple  clrMagenta  clrCyan
clrLime  clrMaroon  clrNavy  clrOlive  clrTeal  clrAqua
clrFuchsia  clrPink  clrGold  clrLavender  clrCoral  clrCrimson
clrDarkGreen  clrDarkBlue  clrDarkRed  clrDodgerBlue  clrFireBrick
clrForestGreen  clrIndigo  clrKhaki  clrMediumBlue  clrNone
```

---

## Chart Constants (ENUM_CHART_...)
```
CHART_IS_OBJECT  CHART_BRING_TO_TOP  CHART_SHIFT  CHART_AUTOSCROLL
CHART_MODE  CHART_FOREGROUND  CHART_SHOW_GRID  CHART_SHOW_VOLUMES
CHART_SHOW_OBJECT_DESCR  CHART_VISIBLE_BARS  CHART_ID
CHART_WINDOW_HANDLE  CHART_FIRST_VISIBLE_BAR  CHART_PRICE_MIN
CHART_PRICE_MAX  CHART_COMMENT  CHART_SCALE  CHART_COLOR_BACKGROUND
```

## Object Types (ENUM_OBJECT)
```
OBJ_VLINE  OBJ_HLINE  OBJ_TREND  OBJ_TRENDBYANGLE  OBJ_CHANNEL
OBJ_STDDEVCHANNEL  OBJ_REGRESSION  OBJ_PITCHFORK  OBJ_GANNLINE
OBJ_GANNFAN  OBJ_GANNGRID  OBJ_FIBO  OBJ_FIBOTIMES  OBJ_FIBOFAN
OBJ_FIBOARC  OBJ_FIBOCHANNEL  OBJ_EXPANSION  OBJ_ELLIPSE
OBJ_ARROW  OBJ_ARROW_BUY  OBJ_ARROW_SELL  OBJ_TEXT  OBJ_LABEL
OBJ_BUTTON  OBJ_CHART  OBJ_BITMAP  OBJ_BITMAP_LABEL  OBJ_EDIT
OBJ_RECTANGLE  OBJ_RECTANGLE_LABEL  OBJ_EVENT
```