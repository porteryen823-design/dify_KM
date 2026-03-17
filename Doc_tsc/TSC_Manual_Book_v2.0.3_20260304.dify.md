![](media/image48.png)

**TSC 操作手冊**

![](media/image47.png) Transfer System Controller

版本： v2.0.2

最近更新： 2025-05-09

目錄

[**系統對應版本 17**](#系統對應版本)

> [版次更新紀錄 17](#版次更新紀錄)

[1. 操作手冊主要內容 19](#操作手冊主要內容)

[2. 系統及基本功能介紹 19](#系統及基本功能介紹)

> [2.1 使用環境與作業系統 19](#使用環境與作業系統)
>
> [2.2 硬體需求 19](#硬體需求)
>
> [2.3 功能與特色說明 20](#功能與特色說明)
>
> [2.4 系統安裝 20](#系統安裝)
>
> [2.5 相關文件 21](#相關文件)

[**3. 開始使用TSC系統 22**](#開始使用tsc系統)

> [3.1 第一次使用，登入畫面 24](#第一次使用登入畫面)
>
> [3.2 主看板 26](#主看板)

[**4. 系統介面說明 28**](#系統介面說明)

> [4.1 主看板 ( Dashboard ) 29](#主看板-dashboard)
>
> [4.1.1 導覽列 29](#導覽列)
>
> [4.1.2 功能列 30](#功能列)
>
> [4.1.2.1 導覽列最大化最小化按鈕 30](#導覽列最大化最小化按鈕)
>
> [4.1.2.2 專案功能選單 30](#專案功能選單)
>
> [4.1.2.2.A 新增專案 ( New Project ) 31](#a-新增專案-new-project)
>
> [4.1.2.2.B 選擇專案 ( Select Project ) 31](#b-選擇專案-select-project)
>
> [4.1.2.2.C 編輯專案 ( Edit Project ) 32](#c-編輯專案-edit-project)
>
> [4.1.2.2.D 匯出專案 ( Export Project ) 32](#d-匯出專案-export-project)
>
> [4.1.2.2.E 匯入專案 ( Import Project ) 32](#e-匯入專案-import-project)
>
> [4.1.2.3 專案名稱 (Project Name) 33](#專案名稱-project-name)
>
> [4.1.2.4 淺色模式與深色模式（Light Mode and Dark Mode） 34](#淺色模式與深色模式light-mode-and-dark-mode)
>
> [4.1.2.5 語言切換（Language Switch） 34](#語言切換language-switch)
>
> [4.1.2.6 警告訊息通知（Warning Message Notification） 34](#警告訊息通知warning-message-notification)
>
> [4.1.2.7 登入狀態（Login Status） 34](#登入狀態login-status)
>
> [4.1.2.8 基本設定圖示（Basic Settings Icon） 35](#基本設定圖示basic-settings-icon)
>
> [4.1.3 主看板內容資訊 36](#主看板內容資訊)
>
> [4.1.3.1 自走車狀態（AMR Status）： 36](#自走車狀態amr-status)
>
> [4.1.3.2 工作站狀態（Workstations Status）： 37](#工作站狀態workstations-status)
>
> [4.1.3.3 電子貨架狀態（Erack Status）： 38](#電子貨架狀態erack-status)
>
> [4.1.3.4 版本與改版資訊（Version and Changelog Information）： 39](#版本與改版資訊version-and-changelog-information)
>
> [4.2 基本設定 ( Settings ) 41](#基本設定-settings)
>
> [4.2.1 管理員資訊 41](#管理員資訊)
>
> [4.2.2 TSC 系統設定 42](#tsc-系統設定)
>
> [4.2.2.1 命令檢查 ( Command Check )： 42](#命令檢查-command-check)
>
> [4.2.2.1.1 白名單 ( CarrierWhiteMask ) 42](#白名單-carrierwhitemask)
>
> [4.2.2.1.2 等待佇列檢查（CarrierDuplicatedInWaitingQueueCheck）： 42](#等待佇列檢查carrierduplicatedinwaitingqueuecheck)
>
> [4.2.2.1.3 執行佇列檢查（CarrierDuplicatedInExcutingQueueCheck）： 42](#執行佇列檢查carrierduplicatedinexcutingqueuecheck)
>
> [4.2.4.1.5 目的地儲位檢查（DestPortDuplicatedCheck）： 43](#目的地儲位檢查destportduplicatedcheck)
>
> [4.2.4.1.6 關聯 Carrier ID 檢查（AssociateCarrierIDCheck）： 43](#關聯-carrier-id-檢查associatecarrieridcheck)
>
> [4.2.4.1.7 啟用自動分配目標儲位（AutoAssignDestPortEnable）： 43](#啟用自動分配目標儲位autoassigndestportenable)
>
> [4.2.2.2 命令調度 ( Command Dispatch )： 49](#命令調度-command-dispatch)
>
> [4.2.4.2.1 DivideDispatchZoneEnable ( 依區域分割調度 ) 49](#dividedispatchzoneenable-依區域分割調度)
>
> [4.2.4.2.2 DivideMethodByMachinePior ( 依指令分割的設定進行調度安排 ) 49](#dividemethodbymachinepior-依指令分割的設定進行調度安排)
>
> [4.2.2.3 晶圓盒規格感測 ( Cassette Type Sensitive )： 49](#晶圓盒規格感測-cassette-type-sensitive)
>
> [4.2.2.3.1 晶圓盒規格感測啟用（CassetteTypeSensitiveEnable）： 50](#晶圓盒規格感測啟用cassettetypesensitiveenable)
>
> [4.2.2.3.2 晶圓盒規格感測方法（CassetteTypeSensitiveMethod）： 50](#晶圓盒規格感測方法cassettetypesensitivemethod)
>
> [4.2.2.3.3 電子貨架晶圓盒類型檢查（ErackCassetteTypeCheck）： 50](#電子貨架晶圓盒類型檢查erackcassettetypecheck)
>
> [4.2.2.4 保護機制 ( Safty )： 51](#保護機制-safty)
>
> [4.2.2.4.1 電子貨架狀態檢查（ErackStatusCheck）： 51](#電子貨架狀態檢查erackstatuscheck)
>
> [4.2.2.4.2 儲位狀態檢查（BufferStatusCheck）： 52](#儲位狀態檢查bufferstatuscheck)
>
> [4.2.2.4.3 預綁定檢查（PreBindCheck）： 52](#預綁定檢查prebindcheck)
>
> [4.2.2.4.4 重命名失敗 ID（RenameFailedID）： 52](#重命名失敗-idrenamefailedid)
>
> [4.2.2.4.5 儲位位置檢查（BufferPosCheck）： 52](#儲位位置檢查bufferposcheck)
>
> [4.2.2.4.6 取消儲位 RFID 檢查（BufferNoRFIDCheck）： 52](#取消儲位-rfid-檢查buffernorfidcheck)
>
> [4.2.2.4.7 來源位置不符檢查（SourceLocationMismatchCheck）： 52](#來源位置不符檢查sourcelocationmismatchcheck)
>
> [4.2.2.4.8 跳過上貨中止時的下貨中止（SkipAbortLoadWhenUnloadAbort）： 52](#跳過上貨中止時的下貨中止skipabortloadwhenunloadabort)
>
> [4.2.2.4.10 斷開時釋放路權（ReleaseRightWhenDisconnected）： 53](#斷開時釋放路權releaserightwhendisconnected)
>
> [4.2.2.4.11 搬運位移檢查（TrShiftReqCheck）： 53](#搬運位移檢查trshiftreqcheck)
>
> [4.2.2.4.12 省略搬運上架檢查（SkipTrLoadReqWhenSwapTask）： 53](#省略搬運上架檢查skiptrloadreqwhenswaptask)
>
> [4.2.2.4.13 搬運上架檢查（TrLoadReqCheck）： 53](#搬運上架檢查trloadreqcheck)
>
> [4.2.2.4.14 搬運上架檢查逾時設定（TrLoadReqTimeout）： 53](#搬運上架檢查逾時設定trloadreqtimeout)
>
> [4.2.2.4.15 搬運下架檢查（TrUnloadReqCheck）： 53](#搬運下架檢查trunloadreqcheck)
>
> [4.2.2.4.16 回傳檢查（TrBackReqCheck）： 53](#回傳檢查trbackreqcheck)
>
> [4.2.2.4.17 設備回傳檢查（TrBackReqCheckForEQ）： 54](#設備回傳檢查trbackreqcheckforeq)
>
> [4.2.2.4.18 回傳檢查逾時設定（TrBackReqTimeout）： 54](#回傳檢查逾時設定trbackreqtimeout)
>
> [4.2.2.4.19 交換任務逾時設定（TrSwapReqTimeout）： 54](#交換任務逾時設定trswapreqtimeout)
>
> [4.2.2.5 批次任務設定 ( Batch Run )：(目前已無作用) 54](#批次任務設定-batch-run-目前已無作用)
>
> [4.2.2.5.1 批次命令大小（Batch Size）： 54](#批次命令大小batch-size)
>
> [4.2.2.5.2 收集命令逾時（Collect Timeout）（單位：秒）： 54](#收集命令逾時collect-timeout單位秒)
>
> [4.2.2.5.3 合併命令起始逾時（Merge Start Timeout）（單位：秒）： 54](#合併命令起始逾時merge-start-timeout單位秒)
>
> [4.2.2.6 失敗復原設定 ( Recovery )： 55](#失敗復原設定-recovery)
>
> [4.2.2.6.1 自動（Auto）： 55](#自動auto)
>
> [4.2.2.6.2 保留載具於車輛上（KeepCarrierOnTheVehicle）： 55](#保留載具於車輛上keepcarrieronthevehicle)
>
> [4.2.2.6.3 異常貨架載具類型檢查（FaultyErackCarrierTypeCheck）： 55](#異常貨架載具類型檢查faultyerackcarriertypecheck)
>
> [4.2.2.6.4 與自走車同步重置（ResetSyncWithMR）： 55](#與自走車同步重置resetsyncwithmr)
>
> [4.2.2.6.5 剩餘殘貨退回至（ResidualReturnTo）： 56](#剩餘殘貨退回至residualreturnto)
>
> [4.2.2.6.6 發生錯誤警示時取消所有命令（AbortAllCommandsWhenErrorAlarm）： 56](#發生錯誤警示時取消所有命令abortallcommandswhenerroralarm)
>
> [4.2.2.6.7 重大錯誤拒絕接收命令（AbortAllCommandsWhenSeriousAlarm）： 56](#重大錯誤拒絕接收命令abortallcommandswhenseriousalarm)
>
> [4.2.2.6.8 發生錯誤警示時取消連結命令（AbortLinkCommandWhenErrorAlarm）： 56](#發生錯誤警示時取消連結命令abortlinkcommandwhenerroralarm)
>
> [4.2.2.6.9 重新分配目的地（ReAssignErackDestPortWhenOccupied）： 56](#重新分配目的地reassignerackdestportwhenoccupied)
>
> [4.2.2.6.10 移動重試（RetryMoveWhenAlarmReset）： 56](#塞車重試retrybackthenforwardwhenjam)
>
> [4.2.2.6.11 塞車重試（RetryBackThenForwardWhenJam）： 56](#塞車重試retrybackthenforwardwhenjam)
>
> [4.2.2.6.12 無有效儲位時返回異常貨架（ReturnToFaultyErackWhenNoValidBuf）： 56](#無有效儲位時返回異常貨架returntofaultyerackwhennovalidbuf)
>
> [4.2.2.6.13 下貨檢查失敗時重試（RetryWhenTrUnloadCheckNG）： 57](#下貨檢查失敗時重試retrywhentrunloadcheckng)
>
> [4.2.2.7 交通管制設定 ( Traffic Control )： 57](#交通管制設定-traffic-control)
>
> [4.2.2.7.1 啟用路口交管功能（Enable Traffic Point）： 57](#啟用路口交管功能enable-traffic-point)
>
> [4.2.2.7.2 自動尋找路徑（Enable Find Way）： 57](#自動尋找路徑enable-find-way)
>
> [4.2.2.7.3 優先選擇直行路線（EnableStraightRoadFirst）： 58](#優先選擇直行路線enablestraightroadfirst)
>
> [4.2.2.7.4 行進角度固定（Keep Angle）： 58](#行進角度固定keep-angle)
>
> [4.2.2.7.5 路權獲取逾時（Get Right Timeout）： 58](#路權獲取逾時get-right-timeout)
>
> [4.2.2.7.6 路權獲取逾時重新尋路（Find Way Time）： 58](#路權獲取逾時重新尋路find-way-time)
>
> [4.2.2.7.7 最大繞路距離（Max Find Way Cost）： 58](#最大繞路距離max-find-way-cost)
>
> [4.2.2.7.8 安全距離（Near Distance）： 58](#安全距離near-distance)
>
> [4.2.2.7.9 持續行進範圍（KeepGoingRange）： 58](#持續行進範圍keepgoingrange)
>
> [4.2.2.7.10 動態釋放路權（Dynamic Release Right）： 58](#動態釋放路權dynamic-release-right)
>
> [4.2.2.7.11 路權釋放來源（Release Right Based On Location）： 58](#路權釋放來源release-right-based-on-location)
>
> [4.2.2.8 通訊設定 ( Communication )： 59](#通訊設定-communication)
>
> [4.2.2.8.1 PS 協定（PS Protocol）： 59](#ps-協定ps-protocol)
>
> [4.2.2.8.2 主機協定（Host Protocol）： 59](#主機協定host-protocol)
>
> [4.2.2.8.3 貨架命名規則（Rack Naming）： 59](#貨架命名規則rack-naming)
>
> [4.2.2.9 其他項目 ( Other )： 60](#其他項目-other)
>
> [4.2.2.9.1 從出發位置回報（ReportFromPortWhenVehicleDeparted）： 60](#從出發位置回報reportfromportwhenvehicledeparted)
>
> [4.2.2.9.2 啟用 SRTD 功能（SRTD Enable）： 60](#啟用-srtd-功能srtd-enable)
>
> [4.2.2.9.3 啟用 Stage 指令（Stage Enable）： 60](#啟用-stage-指令stage-enable)
>
> [4.2.2.9.4 支援 Loadport（Loadport Support）： 61](#支援-loadportloadport-support)
>
> [4.2.2.9.5 預先搬貨指令（PreDispatch）： 61](#預先搬貨指令predispatch)
>
> [4.2.2.9.6 針對電子貨架執行預先搬貨指令（PreDispatchForRack）： 61](#針對電子貨架執行預先搬貨指令predispatchforrack)
>
> [4.2.2.9.7 立即指派請求（ImmediatelyAssignedReq）： 61](#立即指派請求immediatelyassignedreq)
>
> [4.2.2.9.8 啟用站點順序（StationOrderEnable）： 61](#啟用站點順序stationorderenable)
>
> [4.2.2.9.9 跨區域中繼搬運（RelayTransferWhenCrossZone）： 61](#跨區域中繼搬運relaytransferwhencrosszone)
>
> [4.2.2.9.10 自動清除預訂狀態（AutoResetBooked）： 61](#自動清除預訂狀態autoresetbooked)
>
> [4.2.2.9.11 延遲預訂（BookLater）： 61](#延遲預訂booklater)
>
> [4.2.2.9.12 依需求中斷任務（WithdrawJobOnDemand）： 61](#依需求中斷任務withdrawjobondemand)
>
> [4.2.2.9.13 停用 Port2Addr 對照表（DisablePort2AddrTable）： 62](#停用-port2addr-對照表disableport2addrtable)
>
> [4.2.2.9.14 E84 連續取放功能（E84Continue）： 62](#e84-連續取放功能e84continue)
>
> [4.2.2.9.15 EAP 連接（EAPConnect）： 62](#eap-連接eapconnect)
>
> [4.3 工作站( Workstation ) 63](#工作站-workstation)
>
> [4.3.1 匯入工作站（Import Floor Workstations）： 63](#匯入工作站import-floor-workstations)
>
> [4.3.2 匯出工作站（Export Floor Workstations）： 64](#匯出工作站export-floor-workstations)
>
> [4.3.3 手動新增（Add Row 、 Add Column）： 64](#手動新增add-row-add-column)
>
> [4.3.4 工作站表格欄位 ( Work Station Form )： 66](#工作站表格欄位-work-station-form)
>
> [4.3.4.1刪除按鈕（Delete Button）： 66](#刪除按鈕delete-button)
>
> [4.3.4.2 工作站 ID（Workstation ID）： 66](#工作站-idworkstation-id)
>
> [4.3.4.3 設備 ID（Equipment ID）： 66](#設備-idequipment-id)
>
> [4.3.4.4 區域 ID（Zone ID）： 66](#區域-idzone-id)
>
> [4.3.4.5 Stage： 67](#stage)
>
> [4.3.4.6 IP 位址（IP Address）： 67](#ip-位址ip-address)
>
> [4.3.4.7 連接埠（Port）： 67](#連接埠port)
>
> [4.3.4.8 Return to： 67](#return-to)
>
> [4.3.4.9 預先派送（Predispatch）： 67](#預先派送predispatch)
>
> [4.3.4.10 設備進出貨選項： 67](#設備進出貨選項)
>
> [4.3.4.11 有效輸入（Valid Input）： 68](#有效輸入valid-input)
>
> [4.3.4.12 限制擺放位置（Buf Constrain）： 68](#限制擺放位置buf-constrain)
>
> [4.3.4.13 開門輔助（Open Door Assist）： 68](#開門輔助open-door-assist)
>
> [4.3.4.14 允許位移（Allow Shift）： 68](#允許位移allow-shift)
>
> [4.3.4.15 啟用（Enable）： 68](#啟用enable)
>
> [4.3.5 展開全部（Expand All）： 68](#展開全部expand-all)
>
> [4.3.6 切換樓層（下拉選單）： 69](#切換樓層下拉選單)
>
> [4.3.7 存檔（Save）： 69](#存檔save)
>
> [4.4 區域管理 ( Zone Management ) 70](#區域管理-zone-management)
>
> [4.4.1 新增區域功能列 ( Add New Zone )： 70](#新增區域功能列-add-new-zone)
>
> [4.4.2 區域列表： 71](#區域列表)
>
> [4.4.2.1 區域名稱 (Zone Name)： 71](#區域名稱-zone-name)
>
> [4.4.2.2 相鄰區域 (Neighbor Zone)： 71](#相鄰區域-neighbor-zone)
>
> [4.4.2.3 排程演算法（Schedule Algo）： 71](#排程演算法schedule-algo)
>
> [4.4.2.4 車輛演算法（Vehicle Algo）： 72](#車輛演算法vehicle-algo)
>
> [4.4.2.5 最大合併命令數 (Merge Max Cmds)： 72](#最大合併命令數-merge-max-cmds)
>
> [4.4.2.6 任務合併前置時間 (Merge Start Time)： 72](#任務合併前置時間-merge-start-time)
>
> [4.4.2.7 任務合併集結時間 ( Collect Timeout )： 73](#任務合併集結時間-collect-timeout)
>
> [4.4.2.8 最大合併設備數 (Merge Max Eqps)： 73](#最大合併設備數-merge-max-eqps)
>
> [4.4.2.9 指令存活時間（Command Living Time）： 73](#指令存活時間command-living-time)
>
> [4.4.2.10 Action： 73](#action)
>
> [4.5 搬運統計看板 ( Transfer Statistics ) 74](#搬運統計看板-transfer-statistics)
>
> [4.5.1 功能選單 ( Options )： 74](#功能選單-options)
>
> [4.5.1.1 時間篩選 ( Date Time )： 74](#時間篩選-date-time)
>
> [4.5.1.2 重新整理 ( Refresh )： 75](#重新整理-refresh)
>
> [4.5.1.3 自走車切換選單 ( AMR Selection )： 75](#自走車切換選單-amr-selection)
>
> [4.5.2 自走車狀態 ( MR Status )： 75](#自走車狀態-mr-status)
>
> [4.5.3 合併指令 ( Commands Merger )： 77](#合併指令-commands-merger)
>
> [4.5.4 搬運量 ( Transfers )： 77](#搬運量-transfers)
>
> [4.5.4 平均搬運時間 ( Transfers Average Time )： 79](#平均搬運時間-transfers-average-time)
>
> [4.5.5 錯誤代碼 ( Result Code )： 79](#錯誤代碼-result-code)
>
> [4.5.5 當月完成搬運量 ( Transfers Completed This Month )： 80](#當月完成搬運量-transfers-completed-this-month)
>
> [4.5.6 今日警報數量 ( Alarm Frequency Today )： 80](#今日警報數量-alarm-frequency-today)
>
> [4.5.7 距離上次警報時間 ( Time Since Last Alarm )： 81](#距離上次警報時間-time-since-last-alarm)
>
> [4.6 自走車統計看板 ( Vehicle Statistics ) 81](#自走車統計看板-vehicle-statistics)
>
> [4.6.1 功能選單 ( Options )： 81](#功能選單-options-1)
>
> [4.6.1.1 時間篩選 ( Date Time )： 81](#時間篩選-date-time-1)
>
> [4.6.1.2 重新整理 ( Refresh )： 82](#重新整理-refresh-1)
>
> [4.6.1.3 自走車切換選單 ( AMR Selection )： 82](#自走車切換選單-amr-selection-1)
>
> [4.6.2 30天內端口阻塞時間 ( Port Blocking Time In 30 Days )： 82](#天內端口阻塞時間-port-blocking-time-in-30-days)
>
> [4.6.3 車輛數據 ( Vehicle States )： 83](#車輛數據-vehicle-states)
>
> [4.6.4 車輛運行狀態紀錄 ( Vehicle States Logs )： 84](#車輛運行狀態紀錄-vehicle-states-logs)
>
> [4.6.5 車輛警報紀錄 ( Vehicle Alarm Logs )： 85](#車輛警報紀錄-vehicle-alarm-logs)
>
> [4.6.6 電池資訊紀錄 ( Battery Info Logs )： 85](#電池資訊紀錄-battery-info-logs)
>
> [4.6.7 啟動電池數據統計( Starting Battery Statistics )： 85](#啟動電池數據統計-starting-battery-statistics)
>
> [4.6.7.1 電量指示條 ( Battery bar )： 86](#電量指示條-battery-bar)
>
> [4.6.7.2 自走車月平均充電時間 ( Average Charge Time in 30 Days Per Vehicle )： 87](#自走車月平均充電時間-average-charge-time-in-30-days-per-vehicle)
>
> [4.6.7.2.1 過去 30 天內平均充電時間 (Average Charge Time in 30 Days Per Vehicle)： 87](#過去-30-天內平均充電時間-average-charge-time-in-30-days-per-vehicle)
>
> [4.6.7.2.2 每月充電完成次數統計 (Count for Aqurice to Charge Per Vehicle)： 87](#每月充電完成次數統計-count-for-aqurice-to-charge-per-vehicle)
>
> [4.6.7.2.3 充電循環次數 (Number of Charging Cycles Per Vehicle) 87](#充電循環次數-number-of-charging-cycles-per-vehicle)
>
> [4.6.8 電池資訊 ( Vehicle battery information )： 88](#電池資訊-vehicle-battery-information)
>
> [4.6.8.1 電池資訊統計 ( Battery Info Staticstics )： 88](#電池資訊統計-battery-info-staticstics)
>
> [4.6.8.2 電池單元統計 ( Battery Cells Staticstics )： 89](#電池單元統計-battery-cells-staticstics)
>
> [4.7 命令歷史紀錄 ( Transfer Commands ) 90](#命令歷史紀錄-transfer-commands)
>
> [4.7.1 命令紀錄頁籤 ( Commands Tab )： 90](#命令紀錄頁籤-commands-tab)
>
> [4.7.1.1 功能選單 ( Options )： 90](#功能選單-options-2)
>
> [4.7.1.1.1 匯出資料表 ( Export )： 90](#匯出資料表-export)
>
> [4.7.1.1.2 重新整理 ( Refresh )： 90](#重新整理-refresh-2)
>
> [4.7.1.1.3 搜尋 ( Search )： 90](#搜尋-search)
>
> [4.7.1.1.4 資料表 ( Data Table )： 91](#資料表-data-table)
>
> [4.7.2 退回命令紀錄頁籤 ( Rejected Commands Tab )： 91](#退回命令紀錄頁籤-rejected-commands-tab)
>
> [4.8 搬運任務看板（Transfer Dashboard） 92](#搬運任務看板transfer-dashboard)
>
> [4.8.1 等待佇列（Transfer Waiting Queue） 92](#等待佇列transfer-waiting-queue)
>
> [4.8.2 執行佇列 (Transfer Executing Queue) 93](#執行佇列-transfer-executing-queue)
>
> [4.8.3 手動添加單筆任務 ( Manual Input ) 93](#手動添加單筆任務-manual-input)
>
> [4.8.3.1 載具 ID（Carrier ID）： 94](#載具-idcarrier-id)
>
> [4.8.3.2 載具類型（Carrier Type）： 94](#載具類型carrier-type)
>
> [4.8.3.3 優先度（Priority）： 94](#優先度priority)
>
> [4.8.3.4 來源位置（Source）： 94](#來源位置source)
>
> [4.8.3.5 目的地（Destination）： 94](#目的地destination)
>
> [4.8.3.6 交換（Replace）： 94](#交換replace)
>
> [4.8.3.7 返回站點（Back）： 95](#返回站點back)
>
> [4.8.3.8 返回載具 ID（Back Carrier ID）： 95](#返回載具-idback-carrier-id)
>
> [4.8.3.9 返回載具類型（Back Carrier Type）： 95](#返回載具類型back-carrier-type)
>
> [4.8.3.11 新增 ( Add ) ： 95](#新增-add)
>
> [4.8.4 批次執行多筆任務 ( Batch Run ) 97](#批次執行多筆任務-batch-run)
>
> [4.8.5 循環測試任務 ( Test Run ) 99](#循環測試任務-test-run)
>
> [4.9 地圖管理（Map Management） 102](#地圖管理map-management)
>
> [4.9.1 上傳地圖 ( Upload Map ) 102](#上傳地圖-upload-map)
>
> [4.9.2 上傳地圖列表 ( Upload Map ) 102](#上傳地圖列表-upload-map)
>
> [4.9.3 自走車連接上傳 ( AMR Connect Upload ) 103](#自走車連接上傳-amr-connect-upload)
>
> [4.10 地圖編輯（ Map Editor ） 104](#地圖編輯-map-editor)
>
> [4.10.1 地圖功能列 ( Map Options ) 104](#地圖功能列-map-options)
>
> [4.10.1.1 地圖 ( MAP ) 104](#地圖-map)
>
> [4.10.1.1.1 新增樓層 ( New Floor ) 104](#新增樓層-new-floor)
>
> [4.10.1.1.1.1 樓層名稱 ( Level Name )： 105](#樓層名稱-level-name)
>
> [4.10.1.1.1.2 地圖檔案 ( Map File )： 105](#地圖檔案-map-file)
>
> [4.10.1.1.1.3 層級 ( Z-index )： 106](#層級-z-index)
>
> [4.10.1.1.1.4 自走車 IP ( Vehicle IP )： 106](#自走車-ip-vehicle-ip)
>
> [4.10.1.1.1.5 路線檔 ( Local Route File )： 107](#路線檔-local-route-file)
>
> [4.10.1.1.1.6 移動附加設定 ( Move Append )： 108](#移動附加設定-move-append)
>
> [4.10.1.1.2 存檔 ( Save ) 109](#存檔-save)
>
> [4.10.1.1.3 刪除樓層 ( Delete Floor ) 109](#刪除樓層-delete-floor)
>
> [4.10.1.1.4 地圖屬性設定 ( Map Display Settings) 110](#地圖屬性設定-map-display-settings)
>
> [4.10.1.1.4.1 臨界值 ( Threshold ) 110](#臨界值-threshold)
>
> [4.10.1.1.4.2 方向標示顏色 ( Triangle Direction Colour ) 111](#方向標示顏色-triangle-direction-colour)
>
> [4.10.1.1.4.3 站點填充顏色 ( Fill Colour ) 111](#站點填充顏色-fill-colour)
>
> [4.10.1.1.4.4 站點外框顏色 ( Stroke Colour ) 111](#站點外框顏色-stroke-colour)
>
> [4.10.1.1.4.5 站點線條粗細 ( Stroke Width ) 111](#站點線條粗細-stroke-width)
>
> [4.10.1.1.4.6 路徑線條 ( Path Stroke ) 112](#路徑線條-path-stroke)
>
> [4.10.1.1.4.7 方向標示大小 ( Triangle Size \[WxH\] ) 112](#方向標示大小-triangle-size-wxh)
>
> [4.10.1.1.4.8 地圖站點半徑 ( Radius ) 112](#地圖站點半徑-radius)
>
> [4.10.1.1.4.9 站點實心狀態 ( Fill States ) 113](#站點實心狀態-fill-states)
>
> [4.10.1.1.5 更新地圖站點 ( Fix Map Points ) 113](#更新地圖站點-fix-map-points)
>
> [4.10.1.1.5.1 目前地圖站點 ( Current ) 113](#目前地圖站點-current)
>
> [4.10.1.1.5.2 比對地圖站點 ( Different ) 114](#比對地圖站點-different)
>
> [4.10.1.1.6 更換地圖 ( Change Maps ) 115](#更換地圖-change-maps)
>
> [4.10.1.1.7 產生站點標籤 ( Generate Station Label ) 117](#產生站點標籤-generate-station-label)
>
> [4.10.1.1.8 下載 PNG 圖檔 ( Download PNG ) 117](#下載-png-圖檔-download-png)
>
> [4.10.1.2 繪製功能 ( Draw ) 118](#繪製功能-draw)
>
> [4.10.1.2.1 路徑 (Path) 118](#路徑-path)
>
> [4.10.1.2.2 站點 ( Point ) 118](#站點-point)
>
> [4.10.1.2.3 工作站 ( Workstation ) 119](#工作站-workstation-1)
>
> [4.10.1.2.4 錨點 ( Anchor ) 119](#錨點-anchor)
>
> [4.10.1.2.5 鎖定移動（Lock Move） 120](#鎖定移動lock-move)
>
> [4.10.1.2.5 站點移動（Point Move） 120](#站點移動point-move)
>
> [4.10.1.2.5.1 X軸座標修改器 ( X-Avis )： 120](#x軸座標修改器-x-avis)
>
> [4.10.1.2.5.2 Y軸座標修改器 ( Y-Avis )： 120](#y軸座標修改器-y-avis)
>
> [4.10.2 地圖顯示 ( Map Display ) 123](#地圖顯示-map-display)
>
> [4.10.2.1 方向鍵（Arrow Key）： 123](#方向鍵arrow-key)
>
> [4.10.2.2 地圖縮放（Map Zoom）： 123](#地圖縮放map-zoom)
>
> [4.10.2.3 復原（ Undo ）： 123](#復原-undo)
>
> [4.10.2.4 重做（ Redo ）： 123](#重做-redo)
>
> [4.10.3 站點屬性 ( Properties ) 125](#站點屬性-properties)
>
> [4.10.3.1 站點 ID（Point ID）： 125](#站點-idpoint-id)
>
> [4.10.3.2 X 軸座標（X）： 125](#x-軸座標x)
>
> [4.10.3.3 Y 軸座標（Y）： 125](#y-軸座標y)
>
> [4.10.3.4 角度（W）： 125](#角度w)
>
> [4.10.3.5 Z 軸座標（Z）： 126](#z-軸座標z)
>
> [4.10.3.6 路線（Route）： 126](#路線route)
>
> [4.10.3.7 路口點（Junction）： 126](#路口點junction)
>
> [4.10.3.8 強制停車（Go）： 126](#強制停車go)
>
> [4.10.3.9 臨時停車專用（TmpParkOnly）： 126](#臨時停車專用tmpparkonly)
>
> [4.10.3.10 群組（Group）： 126](#群組group)
>
> [4.10.3.11 啟用（Enable）： 126](#啟用enable-1)
>
> [4.10.3.12 上貨里程權重（Unload Order）& 13.下貨里程權重（Load Order）： 126](#上貨里程權重unload-order-13.下貨里程權重load-order)
>
> [4.10.3.14 類型（Type）： 126](#類型type)
>
> [4.10.3.15 區域 (Zone)： 127](#區域-zone)
>
> [4.10.3.16 站點埠口（Ports）： 127](#站點埠口ports)
>
> [4.10.3.16.1 命名標識系統： 127](#命名標識系統)
>
> [4.10.3.16.2 鎖頭符號 ( 啟用 / 未啟用 ) ( Lock )： 127](#鎖頭符號-啟用-未啟用-lock)
>
> [4.10.3.16.3 工作站 ID ( ID )： 127](#工作站-id-id)
>
> [4.10.3.16.4 E84（e84）： 128](#e84e84)
>
> [4.10.3.16.5 CS（CS）：　　 128](#cscs)
>
> [4.10.3.16.6 PN（PN）： 128](#pnpn)
>
> [4.10.3.16.7 眼睛符號（Visible / Invisible）： 128](#眼睛符號visible-invisible)
>
> [4.10.3.16.8 刪除（Delete）： 128](#刪除delete)
>
> [4.10.3.16.9 新增屬性（Add Property）： 128](#新增屬性add-property)
>
> [4.10.4 路徑屬性 ( Route ) 131](#路徑屬性-route)
>
> [4.10.4.1 路徑 ID ( ID)： 131](#路徑-id-id)
>
> [4.10.4.2 路徑長度 ( Weight )： 131](#路徑長度-weight)
>
> [4.10.4.3 啟用路徑 ( Enable )： 131](#啟用路徑-enable)
>
> [4.10.4.4 群組 ( Group )： 132](#群組-group)
>
> [4.10.4.5 線道 ( Road )： 132](#線道-road)
>
> [4.10.4.6 速度 ( Speed )： 132](#速度-speed)
>
> [4.10.4.7 動態迴避 ( Dynamic Avoidance )： 132](#動態迴避-dynamic-avoidance)
>
> [4.10.4.8 允許逆向超車 ( Reverse Overtaking Allowed )： 132](#允許逆向超車-reverse-overtaking-allowed)
>
> [4.10.4.9 站點 ID ( Point ID )： 132](#站點-id-point-id)
>
> [4.10.4.10 路徑方向 ( Dir )： 133](#路徑方向-dir)
>
> [4.10.4.11 座標 ( X )： 133](#座標-x)
>
> [4.10.4.12 座標 ( Y )： 133](#座標-y)
>
> [4.10.4.13 兩端站點屬性 ( Point Property )： 133](#兩端站點屬性-point-property)
>
> [4.10.4.14 增加屬性欄位 ( Add Property )： 134](#增加屬性欄位-add-property)
>
> [4.10.5 現有站點列表 ( Points ) 136](#現有站點列表-points)
>
> [4.11 自走車看板（ Vehicle Dashboard） 137](#自走車看板-vehicle-dashboard)
>
> [4.11.1 TSC 控制列 ( TSC Control )： 137](#tsc-控制列-tsc-control)
>
> [4.101.1.1 TSC 程式運行狀態（TSC Program Status）： 137](#tsc-程式運行狀態tsc-program-status)
>
> [4.11.1.1.1 TSC 啟動中（TSCInitiated）： 137](#tsc-啟動中tscinitiated)
>
> [4.11.1.1.2 TSC 暫停中（TSCPaused）： 138](#tsc-暫停中tscpaused)
>
> [4.11.1.1.3 TSC 暫停中（TSCPausing）： 138](#tsc-暫停中tscpausing)
>
> [4.11.1.1.4 TSC 自動運行中（TSCAuto）： 138](#tsc-自動運行中tscauto)
>
> [4.11.1.1.5 TSC 離線中（TSCOffline）： 138](#tsc-離線中tscoffline)
>
> [4.11.1.2 TSC 與 Host 之間的底層通訊（TSC-Host Communication）： 138](#tsc-與-host-之間的底層通訊tsc-host-communication)
>
> [4.11.1.2.1 未通訊中（NOT_COMMUNICATING）： 138](#未通訊中not_communicating)
>
> [4.11.1.2.1 通訊中（COMMUNICATING）： 138](#通訊中communicating)
>
> [4.11.1.3 TSC 與 Host 之間的控制狀態（TSC-Host Control Status）： 138](#tsc-與-host-之間的控制狀態tsc-host-control-status)
>
> [4.11.1.3.1 線上遠端控制中（ONLINE_REMOTE）： 138](#線上遠端控制中online_remote)
>
> [4.11.1.3.2 Host 離線中（HOST_OFFLINE）： 138](#host-離線中host_offline)
>
> [4.11.2 地圖顯示頁面 ( Map Display )： 139](#地圖顯示頁面-map-display)
>
> [4.11.2.1 點位操作 (Nodes Actions)： 140](#點位操作-nodes-actions)
>
> [4.11.2.2 路徑操作 (Path Actions)： 140](#路徑操作-path-actions)
>
> [4.11.3 自走車選單 ( AMR List )： 141](#自走車選單-amr-list)
>
> [4.11.4 自走車命令選項 ( AMR Control )： 141](#自走車命令選項-amr-control)
>
> [4.11.5 自走車任務狀態 ( Task )： 142](#自走車任務狀態-task)
>
> [4.11.6 自走車車輛狀態 ( Vehicle Status )： 142](#自走車車輛狀態-vehicle-status)
>
> [4.11.6.1 自走車狀態列表 ( Vehicle Status List)： 142](#自走車狀態列表-vehicle-status-list)
>
> [4.11.6.2 自走車狀態列表 ( Vehicle Status List)： 143](#自走車狀態列表-vehicle-status-list-1)
>
> [4.11.6.3 移動狀態（Move Status）： 143](#移動狀態move-status)
>
> [4.11.6.4 機械臂狀態（Robot Status）： 143](#機械臂狀態robot-status)
>
> [4.11.6.5 電壓檢測（Voltage）： 144](#電壓檢測voltage)
>
> [4.11.6.6 電流檢測（Current）： 144](#電流檢測current)
>
> [4.11.7 自走車錯誤狀態與版本資訊 ( Message )： 144](#自走車錯誤狀態與版本資訊-message)
>
> [4.11.7.1 訊息顯示 (Message)： 144](#訊息顯示-message)
>
> [4.11.7.1 所在站點 (Station)： 144](#所在站點-station)
>
> [4.11.7.1 位置點 (Point)： 144](#位置點-point)
>
> [4.11.7.1 電池狀態 (Battery)： 144](#電池狀態-battery)
>
> [4.11.7.1 健康狀態 (Health)： 144](#健康狀態-health)
>
> [4.11.8 自走車儲位狀態 ( Ports )： 144](#自走車儲位狀態-ports)
>
> [4.11.8.1 自走車儲位狀態 ( Ports )： 145](#自走車儲位狀態-ports-1)
>
> [4.11.9 自走車定位姿態 ( Pose )： 145](#自走車定位姿態-pose)
>
> [4.11.9.1 X軸座標 (X)： 145](#x軸座標-x)
>
> [4.11.9.2 Y軸座標 (Y )： 145](#y軸座標-y)
>
> [4.11.9.3 旋轉角度 (W )： 145](#旋轉角度-w)
>
> [4.11.9.3 高度參數 (Z )： 145](#高度參數-z)
>
> [4.11.10 自走車相機 ( Camera )： 145](#自走車相機-camera)
>
> [4.12 自走車管理（ Vehicle Management） 146](#自走車管理-vehicle-management)
>
> [4.12.1 自走車管理列表 ( AMR Manage ) 146](#自走車管理列表-amr-manage)
>
> [4.12.1.1 自走車資訊 ( 綠色區塊 )： 146](#自走車資訊-綠色區塊)
>
> [4.12.1.1.1 自走車 ID (Vehicle ID)： 146](#自走車-id-vehicle-id)
>
> [4.12.1.1.2 網路通訊IP位址 (IP)： 146](#網路通訊ip位址-ip)
>
> [4.12.1.1.3 通訊連接埠號 (Port)： 146](#通訊連接埠號-port)
>
> [4.12.1.1.4 指定充電站位置 (Charge Station： 146](#指定充電站位置-charge-station)
>
> [4.12.1.1.5 預設運作樓層 (Default Floor)： 146](#預設運作樓層-default-floor)
>
> [4.12.1.1.6 服務區域範圍 (Service Zone)： 146](#服務區域範圍-service-zone)
>
> [4.12.1.1.7 待命點位置 (Standby Station)： 146](#待命點位置-standby-station)
>
> [4.12.1.1.8 緊急避難站點 (Evacuate Station)： 147](#緊急避難站點-evacuate-station)
>
> [4.12.1.1.9 載貨異常處理貨架 (Load Fault Erack)： 147](#載貨異常處理貨架-load-fault-erack)
>
> [4.12.1.1.10 卸貨異常處理貨架 (Unload Fault Erack)： 147](#卸貨異常處理貨架-unload-fault-erack)
>
> [4.12.1.1.11 車輛型號規格 (Model)： 147](#車輛型號規格-model)
>
> [4.12.1.1.12 是否啟用緩衝區功能 (EnableBuffer)： 147](#是否啟用緩衝區功能-enablebuffer)
>
> [4.12.1.1.13 緩衝區類型設定 (Buffer Type)： 147](#緩衝區類型設定-buffer-type)
>
> [4.12.1.1.14 最大運行速度 (Max Speed)： 147](#最大運行速度-max-speed)
>
> [4.12.1.1.15 機械臂操作逾時時間 (Robot Timeout)： 147](#機械臂操作逾時時間-robot-timeout)
>
> [4.12.1.1.16 呼叫支援延遲時間 (Call Support Delay)： 147](#呼叫支援延遲時間-call-support-delay)
>
> [4.12.1.1.17 任務優先權等級 (Priority)： 147](#任務優先權等級-priority)
>
> [4.12.1.1.18 連線重試次數 (Connect Retry)： 147](#連線重試次數-connect-retry)
>
> [4.12.1.1.19 是否啟用起始標記 (Enable Begin Flag)： 148](#是否啟用起始標記-enable-begin-flag)
>
> [4.12.1.1.20 是否允許追加任務 (Append Transfer Allowed)： 148](#是否允許追加任務-append-transfer-allowed)
>
> [4.12.1.1.21 追加任務演算法 (Append Transfer Algo)： 148](#追加任務演算法-append-transfer-algo)
>
> [4.12.1.1.22 是否執行載具類型檢查 (Carrier Type Check)： 148](#是否執行載具類型檢查-carrier-type-check)
>
> [4.12.1.1.23 是否啟用車輛 (Enable)： 148](#是否啟用車輛-enable)
>
> [4.12.1.1.24 編輯功能 (Action)： 148](#編輯功能-action)
>
> [4.12.1.2 自走車充電資訊 ( 紅色區塊 )： 148](#自走車充電資訊-紅色區塊)
>
> [4.12.1.2.1 自動充電 (Auto):: 148](#自動充電-auto)
>
> [4.12.1.2.2 每趟充電 (Every Round): 148](#每趟充電-every-round)
>
> [4.12.1.2.3 最短充電時間 (Minimum Time): 148](#最短充電時間-minimum-time)
>
> [4.12.1.2.4 低電量閾值 (Below Power): 148](#低電量閾值-below-power)
>
> [4.12.1.2.5 最低電量運行 (Run After Minimum Power): 148](#最低電量運行-run-after-minimum-power)
>
> [4.12.1.2.6 閒置時充電 (When Idle): 149](#閒置時充電-when-idle)
>
> [4.12.1.2.7 進入閒置時間 (Into Idle Time): 149](#進入閒置時間-into-idle-time)
>
> [4.12.1.2.8 電池高電量 (Battery High Level): 149](#電池高電量-battery-high-level)
>
> [4.12.1.2.9 充電安全檢查 (Charge Safety Check): 149](#充電安全檢查-charge-safety-check)
>
> [4.12.1.2.10 最長充電時間 (Max Time): 149](#最長充電時間-max-time)
>
> [4.12.1.2.11 電壓範圍 (Voltage (Min / Max)): 149](#電壓範圍-voltage-min-max)
>
> [4.12.1.2.12 電流範圍 (Current (Min / Max)): 149](#電流範圍-current-min-max)
>
> [4.12.1.2.13 排程充電 (Schedule Charging): 149](#排程充電-schedule-charging)
>
> [4.12.1.2.14 排程充電時間 (Schedule Charging Time): 149](#排程充電時間-schedule-charging-time)
>
> [4.12.1.2.15 停靠充電 (Park): 149](#停靠充電-park)
>
> [4.12.1.2.16 待命時充電 (When Standby): 149](#待命時充電-when-standby)
>
> [4.12.1.2.17 進入待命時間 (Into Standby Time): 149](#進入待命時間-into-standby-time)
>
> [4.12.2 新增自走車 ( Add New Vehicle ) 150](#新增自走車-add-new-vehicle)
>
> [4.12.2.1 自走車 ID（Vehicle ID）： 150](#自走車-idvehicle-id)
>
> [4.12.2.2 IP 位址（IP）： 150](#ip-位址ip)
>
> [4.12.2.3 連接埠（Port）： 150](#連接埠port-1)
>
> [4.12.2.4 機器人超時（Robot Timeout）： 150](#機器人超時robot-timeout)
>
> [4.12.2.5 呼叫支援延遲（Call Support Delay）： 151](#呼叫支援延遲call-support-delay)
>
> [4.12.2.6 優先度（Priority）： 151](#優先度priority-1)
>
> [4.12.2.7 裝貨異常貨架（Load Fault Erack）& 卸貨異常貨架（Unload Fault Erack）： 151](#裝貨異常貨架load-fault-erack-卸貨異常貨架unload-fault-erack)
>
> [4.12.2.8 最大速度（Max Speed）： 151](#最大速度max-speed)
>
> [4.12.2.9 重新連線次數（Connect Retry）： 151](#重新連線次數connect-retry)
>
> [4.12.2.10 服務區域（Service Zone）： 151](#服務區域service-zone)
>
> [4.12.2.11 預設樓層（Default Floor）： 152](#預設樓層default-floor)
>
> [4.12.2.12 充電站（Charge Station）： 152](#充電站charge-station)
>
> [4.12.2.13 待命點（Standby Station）： 152](#待命點standby-station)
>
> [4.12.2.14 緊急避難點（Evacuate Station）： 155](#緊急避難點evacuate-station)
>
> [4.12.2.15 型號（Model）： 156](#型號model)
>
> [4.12.2.15.1 啟用儲位（Enable Buffer）： 156](#啟用儲位enable-buffer)
>
> [4.12.2.15.2 儲位類型（Buffer Type）： 157](#儲位類型buffer-type)
>
> [4.12.2.16 充電設定（Charge）： 157](#充電設定charge)
>
> [4.12.2.16.1 自動充電模式 (Auto)： 157](#自動充電模式-auto)
>
> [4.12.2.16.2 每趟任務充電 (Every Round)： 158](#每趟任務充電-every-round)
>
> [4.12.2.16.3 最低充電時間 (Minimum Charge Time)： 158](#最低充電時間-minimum-charge-time)
>
> [4.12.2.16.4 低電量充電閾值 (Charge Below Power)： 158](#低電量充電閾值-charge-below-power)
>
> [4.12.2.16.5 最低運行電量 (Run After Minimum Power)： 158](#最低運行電量-run-after-minimum-power)
>
> [4.12.2.16.6 閒置時充電 (Charge When Idle)： 158](#閒置時充電-charge-when-idle)
>
> [4.12.2.16.7 進入閒置時間 (Into Idle Time)： 158](#進入閒置時間-into-idle-time-1)
>
> [4.12.2.16.8 電池充飽上限 (Battery High Level)： 158](#電池充飽上限-battery-high-level)
>
> [4.12.2.16.9 充電安全檢查 (Charge Safety Check)： 158](#充電安全檢查-charge-safety-check-1)
>
> [4.12.2.16.10 最長充電時間 (Charge Time Max)： 158](#最長充電時間-charge-time-max)
>
> [4.12.2.16.11 最低工作電壓 (Voltage Min)： 158](#最低工作電壓-voltage-min)
>
> [4.12.2.16.12 最高作電壓 (Voltage Max)： 158](#最高作電壓-voltage-max)
>
> [4.12.2.16.13 最低充電電流 (Current Min)： 158](#最低充電電流-current-min)
>
> [4.12.2.16.14 最高充電電流 (Current Max)： 159](#最高充電電流-current-max)
>
> [4.12.2.16.15 排程充電功能 (Enable Schedule Charging)： 159](#排程充電功能-enable-schedule-charging)
>
> [4.12.2.17 停車設定 (Park)： 159](#停車設定-park)
>
> [4.12.2.17.1 待命時停車 (Park When Standby)： 159](#待命時停車-park-when-standby)
>
> [4.12.2.17.2 進入待命時間 (Into Standby Time)： 159](#進入待命時間-into-standby-time-1)
>
> [4.12.2.18 路線設定 (Route)： 159](#路線設定-route)
>
> [4.12.2.18.1 自動重新規劃路線（Auto Rerouting）： 159](#自動重新規劃路線auto-rerouting)
>
> [4.12.2.18.2 警告阻塞時間（Warning Block Time）： 159](#警告阻塞時間warning-block-time)
>
> [4.12.2.18.3 僅頭尾站點（From To Only）： 159](#僅頭尾站點from-to-only)
>
> [4.12.2.19 啟用移位退站（Enable Begin Flag）： 160](#啟用移位退站enable-begin-flag)
>
> [4.12.2.20 允許附加搬運（Append Transfer Allowed）： 160](#允許附加搬運append-transfer-allowed)
>
> [4.12.2.21 載具類型檢查（Carrier Type Check）： 160](#載具類型檢查carrier-type-check)
>
> [4.12.2.22 啟用（Enable）： 160](#啟用enable-2)
>
> [4.12.2.23 新增自走車按鈕（Add Vehicle）： 160](#新增自走車按鈕add-vehicle)
>
> [4.13 電子貨架看板 ( eRack Dashboard ) 161](#電子貨架看板-erack-dashboard)
>
> [4.13.1 TSC 控制列 ( TSC Control )： 161](#tsc-控制列-tsc-control-1)
>
> [4.13.2 Carrier ID 搜尋 ( Search Carrier ID )： 161](#carrier-id-搜尋-search-carrier-id)
>
> [4.13.3 電子貨架列表 (E-Rack List)： 162](#電子貨架列表-e-rack-list)
>
> [4.13.4 電子貨架資訊 (E-Rack Detail)： 162](#電子貨架資訊-e-rack-detail)
>
> [4.13.4.1 現場 Erack 畫面 ( Erack Webpage )： 162](#現場-erack-畫面-erack-webpage)
>
> [4.13.4.2 儲位資訊( Lot Info )： 162](#儲位資訊-lot-info)
>
> [4.13.4.2.1 L1 C4 R1： 163](#l1-c4-r1)
>
> [4.13.4.2.2 08C11138： 163](#c11138)
>
> [4.13.4.2.3 右上角 ✔ ： 163](#右上角)
>
> [4.13.4.2.4 Lot ID： 163](#lot-id)
>
> [4.13.4.2.5 Queue Time： 163](#queue-time)
>
> [4.13.4.2.6 Next Stage： 163](#next-stage)
>
> [4.13.4.2.7 Description： 163](#description)
>
> [4.13.4 電子貨架狀態 (E-Rack Status)： 163](#電子貨架狀態-e-rack-status)
>
> [4.14 電子貨架管理 ( eRack Management ) 165](#電子貨架管理-erack-management)
>
> [4.14.1 匯入電子貨架( Import Racks ) 165](#匯入電子貨架-import-racks)
>
> [4.14.2 手動添加貨架( Add Rack ) 166](#手動添加貨架-add-rack)
>
> [4.14.2.1 設備 ID（Device ID）\*必填項目： 166](#設備-iddevice-id必填項目)
>
> [4.14.2.2 群組 ID（Group ID）\*必填項目： 166](#群組-idgroup-id必填項目)
>
> [4.14.2.3 位置（Location）\*必填項目： 166](#位置location必填項目)
>
> [4.14.2.4 電子貨架設備識別碼（MAC Address）\*必填項目： 167](#電子貨架設備識別碼mac-address必填項目)
>
> [4.14.2.5 貨架流水編號（Serial Number）\*必填項目： 167](#貨架流水編號serial-number必填項目)
>
> [4.14.2.6 IP 位址（IP Address）\*必填項目： 167](#ip-位址ip-address必填項目)
>
> [4.14.2.7 連接埠（Port）\*必填項目： 167](#連接埠port必填項目)
>
> [4.14.2.8 貨架功能選項（Function）\*必填項目： 167](#貨架功能選項function必填項目)
>
> [4.14.2.9 樓層（Floor）\*必填項目： 167](#樓層floor必填項目)
>
> [4.14.2.10 區域（Zone）\*必填項目： 167](#區域zone必填項目)
>
> [4.14.2.11 型號（Model）\*必填項目： 168](#型號model必填項目)
>
> [4.14.2.12 有效儲位類型（Valid Slot Type）\*必填項目： 168](#有效儲位類型valid-slot-type必填項目)
>
> [4.14.2.13 樓層（Floor）\*必填項目： 168](#樓層floor必填項目-1)
>
> [4.14.2.14 連結（Link）\*必填項目： 168](#連結link必填項目)
>
> [4.14.2.15 電子貨架尺寸（Size）\*必填項目： 168](#電子貨架尺寸size必填項目)
>
> [4.14.2.16 分區群組（Sector）非必選項目： 168](#分區群組sector非必選項目)
>
> [4.14.2.17 高水位（Water Level High）： 168](#高水位water-level-high)
>
> [4.14.2.18 低水位（Water Level Low）： 169](#低水位water-level-low)
>
> [4.14.2.19 水位警報（Alarm for Water Level）： 169](#水位警報alarm-for-water-level)
>
> [4.14.2.20 啟用（Enable）非必選項目： 169](#啟用enable非必選項目)
>
> [4.14.2.21 自動派送（Auto Dispatch）： 169](#自動派送auto-dispatch)
>
> [4.14.2.22 批次大小（Batch Size）： 169](#批次大小batch-size)
>
> [4.14.2.23 返回至（Return To）： 169](#返回至return-to)
>
> [4.14.3 分區管理（Sector Management） 170](#分區管理sector-management)
>
> [4.14.3.1 新增分區 (Add Sector)： 170](#新增分區-add-sector)
>
> [4.14.3.2 全部儲存 (Save All)： 170](#全部儲存-save-all)
>
> [4.14.3.3 分區列表 (Sectors)： 170](#分區列表-sectors)
>
> [4.14.3.3.1 分區名稱 (Sector Name)： 170](#分區名稱-sector-name)
>
> [4.14.3.3.2 區域顏色 (Sector Color)： 170](#區域顏色-sector-color)
>
> [4.14.3.3.3 高水位設定 (Water Level High)： 170](#高水位設定-water-level-high)
>
> [4.14.3.3.4 低水位設定 (Water Level Low)： 170](#低水位設定-water-level-low)
>
> [4.14.3.3.5 水位警報 (Alarm for Water Level)： 171](#水位警報-alarm-for-water-level)
>
> [4.14.3.3.6 動作設定 (Action)： 171](#動作設定-action)
>
> [4.14.4 載具管理（Carrier Management） 171](#載具管理carrier-management)
>
> [4.14.4.1 選擇檔案 (Choose a file)： 171](#選擇檔案-choose-a-file)
>
> [4.14.4.2 產生範例檔案 (Generate Example file)： 171](#產生範例檔案-generate-example-file)
>
> [4.14.4.3 清除 (Clear)： 171](#清除-clear)
>
> [4.14.4.4 匯入 (Import)： 172](#匯入-import)
>
> [4.14.4.5 匯出 (Export)： 172](#匯出-export)
>
> [4.15 物聯網設備管理 ( IOT Device Management ) 172](#物聯網設備管理-iot-device-management)
>
> [4.15.1 物聯網設備列表 ( IOT Device List ) 172](#物聯網設備列表-iot-device-list)
>
> [4.15.1.1 控制設備 (Controller)： 172](#控制設備-controller)
>
> [4.15.1.2 裝置 ID (Device ID)： 172](#裝置-id-device-id)
>
> [4.15.1.3 裝置類型 (Device Type)： 172](#裝置類型-device-type)
>
> [4.15.1.4 裝置型號 (Device Model)： 172](#裝置型號-device-model)
>
> [4.15.1.5 IP 位址 (IP)： 173](#ip-位址-ip)
>
> [4.15.1.6 通訊埠 (Port)： 173](#通訊埠-port)
>
> [4.15.1.7 重試次數 (Retry Time)： 173](#重試次數-retry-time)
>
> [4.15.1.8 通訊逾時 (Socket Timeout)： 173](#通訊逾時-socket-timeout)
>
> [4.15.1.9 通訊類型 (Comm Type)： 173](#通訊類型-comm-type)
>
> [4.15.1.10 狀態 (Status)： 173](#狀態-status)
>
> [4.15.1.11 啟用 (Enable)： 173](#啟用-enable)
>
> [4.15.1.12 操作 (Action)： 173](#操作-action)
>
> [4.15.2 新增設備 (Add New Device) 174](#新增設備-add-new-device)
>
> [4.15.2.1.1 電池交換站 (ABCS)： 175](#電池交換站-abcs)
>
> [4.15.2.1.2 電梯控制專用系統 (ELV)： 175](#電梯控制專用系統-elv)
>
> [4.15.2.1.3 工業烤箱主控制器 (OVEN)： 176](#工業烤箱主控制器-oven)
>
> [4.15.2.1.4 烤箱輔助控制介面 (OVENAdapter)： 176](#烤箱輔助控制介面-ovenadapter)
>
> [4.15.2.1.5 門禁系統閘道控制器 (GATE)： 177](#門禁系統閘道控制器-gate)
>
> [4.15.2.1.5.1 通訊類型 (Comm Type)： 177](#通訊類型-comm-type-1)
>
> [4.15.2.1.5.2 需要登入 (Comm Type)： 177](#需要登入-comm-type)
>
> [4.15.2.1.6 空間環境控制系統 (CTRLSPACE)： 178](#空間環境控制系統-ctrlspace)
>
> [4.15.3 編輯設備 (Edit Device) 179](#編輯設備-edit-device)
>
> [4.15.3.1.1 電池交換站 (ABCS) 179](#電池交換站-abcs-1)
>
> [4.15.3.1.2 電梯控制專用系統 (ELV) 179](#電梯控制專用系統-elv-1)
>
> [4.15.3.1.3 工業烤箱主控制器 (OVEN) 180](#工業烤箱主控制器-oven-1)
>
> [4.15.3.1.4 烤箱輔助控制介面 (OVENAdapter) 180](#烤箱輔助控制介面-ovenadapter-1)
>
> [4.15.3.1.5 門禁系統閘道控制器 (GATE) 181](#門禁系統閘道控制器-gate-1)
>
> [4.15.3.1.6 空間環境控制系統 (CTRLSPACE) 181](#空間環境控制系統-ctrlspace-1)
>
> [4.16 設備維護 ( Components Maintain ) 182](#設備維護-components-maintain)
>
> [4.16.1 定期維護排程 (Scheduled Maintenance)： 182](#定期維護排程-scheduled-maintenance)
>
> [4.16.1.1 例行性維護 (Routine Maintenance)： 182](#例行性維護-routine-maintenance)
>
> [4.16.1.2 通知時間設定 (Inform Time)： 182](#通知時間設定-inform-time)
>
> [4.16.1.3 操作 (Action)： 182](#操作-action-1)
>
> [4.16.2 自走車零組件用量設定 (Vehicle Component)： 183](#自走車零組件用量設定-vehicle-component)
>
> [4.16.2.1 填寫基本資訊 (Vehicle Components Change Form)： 184](#填寫基本資訊-vehicle-components-change-form)
>
> [4.16.2.2 用量設定 (Setting Usage Amount)： 184](#用量設定-setting-usage-amount)
>
> [4.16.3 車輛元件維護歷史 (Vehicle Component History)： 186](#車輛元件維護歷史-vehicle-component-history)
>
> [4.17 帳號管理 ( Account Management ) 187](#帳號管理-account-management)
>
> [4.17.1 使用者管理 ( User Manegement ) 187](#使用者管理-user-manegement)
>
> [4.17.1.1 列表功能 (Options)： 187](#列表功能-options)
>
> [4.17.1.1.1 切換每頁筆數 (Entries Select)： 187](#切換每頁筆數-entries-select)
>
> [4.17.1.1.2 資料搜尋 (Search)： 187](#資料搜尋-search)
>
> [4.17.1.2 使用者管理列表 (User List)： 187](#使用者管理列表-user-list)
>
> [4.17.1.2.1 登入帳號 (Login ID)： 187](#登入帳號-login-id)
>
> [4.17.1.2.2 帳號權限類別 (Account Type)： 188](#帳號權限類別-account-type)
>
> [4.17.1.2.3 帳號創建時間 (Created At)： 188](#帳號創建時間-created-at)
>
> [4.17.1.2.4 編輯功能 (Action)： 188](#編輯功能-action-1)
>
> [4.17.1.2.4.1 編輯 (Edit)： 188](#編輯-edit)
>
> [4.17.1.2.4.2 刪除 (Delete)： 188](#刪除-delete)
>
> [4.17.1.3 重新整理 (Refresh)： 189](#重新整理-refresh-3)
>
> [4.17.1.4 新增使用者 (New)： 189](#新增使用者-new)
>
> [4.17.1.1.1 登入帳號 (Login ID)： 189](#登入帳號-login-id-1)
>
> [4.17.1.1.2 顯示名稱 (Name)： 189](#顯示名稱-name)
>
> [4.17.1.1.3 登入帳號 (Login ID)： 189](#登入帳號-login-id-2)
>
> [4.17.1.1.4 帳號權限類別 (Account Type)： 189](#帳號權限類別-account-type-1)
>
> [4.17.1.1.5 密碼 (Password)： 190](#密碼-password)
>
> [4.17.1.1.6 確認密碼 (Confirm Password)： 190](#確認密碼-confirm-password)
>
> [4.17.1.1.7 新增使用者 (Add New User)： 190](#新增使用者-add-new-user)
>
> [4.17.1.1.8 取消 (Cancel)： 190](#取消-cancel)
>
> [4.17.2 權限設定 ( Permissions Settings ) 190](#權限設定-permissions-settings)
>
> [4.17.2.1 權限群組下拉選單 (Group Selection Dropdown)： 190](#權限群組下拉選單-group-selection-dropdown)
>
> [4.17.2.2 重新整理 (Refresh)： 190](#重新整理-refresh-4)
>
> [4.17.2.3 編輯權限 (Edit Permissions)： 191](#編輯權限-edit-permissions)
>
> [4.17.3 權限等級 ( Account Type ) 192](#權限等級-account-type)
>
> [4.17.3.1 修改帳號群組 (Edit Account Group) 192](#修改帳號群組-edit-account-group)
>
> [4.17.3.2 刪除帳號群組 (Delete Account Group) 192](#刪除帳號群組-delete-account-group)
>
> [4.17.3.3 重新整理 (Refresh)： 192](#重新整理-refresh-5)
>
> [4.17.3.4 新增帳號群組 (Add New Account Group) 193](#新增帳號群組-add-new-account-group)
>
> [4.18 系統記錄管理 ( Log Management ) 194](#系統記錄管理-log-management)
>
> [4.18.1 時間篩選 (Time Search)： 194](#時間篩選-time-search)
>
> [4.18.2 搜尋 (Search)： 194](#搜尋-search-1)
>
> [4.18.3 日誌列表 (Log List)： 194](#日誌列表-log-list)
>
> [4.18.3.1 紀錄 ID (ID)： 194](#紀錄-id-id)
>
> [4.18.3.2 命令 ID (Command ID)： 194](#命令-id-command-id)
>
> [4.18.3.3 任務事件類型選擇 (Select Type)： 195](#任務事件類型選擇-select-type)
>
> [4.18.3.4 訊息內容 (Message)： 197](#訊息內容-message)
>
> [4.18.3.3 日誌狀態選擇 (Select Type)： 197](#日誌狀態選擇-select-type)
>
> [4.18.3.3.1 資訊 (INFO)： 197](#資訊-info)
>
> [4.18.3.3.2 警告 (WARNING)： 198](#警告-warning)
>
> [4.18.3.3.3 錯誤 (ERROR)： 198](#錯誤-error)
>
> [4.18.3.3.4 嚴重錯誤 (SERIOUS)： 198](#嚴重錯誤-serious)
>
> [4.18.3.5 使用者 (User)： 198](#使用者-user)
>
> [4.18.3.5 建立時間 (Created At)： 198](#建立時間-created-at)
>
> [4.18.4 重新整理 (Refresh)： 198](#重新整理-refresh-6)
>
> [4.18.5 匯出檔案 (Export)： 198](#匯出檔案-export)
>
> [4.19 系統記錄下載 ( Log Files ) 199](#系統記錄下載-log-files)
>
> [4.19.1 日誌檔案下載 ( Download LogFiles )： 199](#日誌檔案下載-download-logfiles)
>
> [4.19.2 日誌檔案搜尋 ( Search LogFiles )： 199](#日誌檔案搜尋-search-logfiles)
>
> [4.19.3 日誌檔案列表 ( LogFiles List )： 199](#日誌檔案列表-logfiles-list)
>
> [4.19.3.1 檔案名稱 (Filename)： 199](#檔案名稱-filename)
>
> [4.19.3.2 目錄路徑 (Directory)： 199](#目錄路徑-directory)
>
> [4.19.3.3 檔案大小 (Size)： 200](#檔案大小-size)
>
> [4.19.3.4 最後修改時間 (Last Modified)： 200](#最後修改時間-last-modified)
>
> [4.19.3.5 操作功能 (Action)： 200](#操作功能-action)
>
> [4.19.4 選擇資料夾 ( Select Folder )： 200](#選擇資料夾-select-folder)
>
> [4.19.5 重新設定 ( Reset )： 200](#重新設定-reset)
>
> [4.19.6 連結自走車 ( Connect AMR )： 200](#連結自走車-connect-amr)
>
> [4.19.7 目前所在資料夾 ( Current Folder )： 200](#目前所在資料夾-current-folder)
>
> [4.19.8 自走車日誌檔列表 ( AMR Log List )： 200](#自走車日誌檔列表-amr-log-list)

[**5. 概念說明 201**](#概念說明)

> [5.1 交通管制概念介紹（Traffic Control Concepts） 201](#交通管制概念介紹traffic-control-concepts)
>
> [5.1.1 車輛行車規則（Vehicle Driving Rules）： 201](#車輛行車規則vehicle-driving-rules)
>
> [5.1.1.1 車輛行車規則（Vehicle Driving Rules）： 201](#車輛行車規則vehicle-driving-rules-1)
>
> [5.1.1.1.1 車輛走行 (Vehicle Movement)： 201](#車輛走行-vehicle-movement)
>
> [5.1.1.1.2 直行判定 (Straight Movement Judgment)： 201](#直行判定-straight-movement-judgment)
>
> [5.1.1.1.3 轉彎設定 (Turning Configuration)： 202](#轉彎設定-turning-configuration)
>
> [5.1.1.2 Keep/Go 點（Keep/Go Points）： 202](#keepgo-點keepgo-points)
>
> [5.1.1.3 路權（Right of Way）： 202](#路權right-of-way)
>
> [5.1.1.3.1 基本原則 (Basic Principle)： 203](#基本原則-basic-principle)
>
> [5.1.1.3.2 路權類型 (Right-of-Way Types)： 203](#路權類型-right-of-way-types)
>
> [5.1.1.3.3 運作流程 (Operation Flow)： 203](#運作流程-operation-flow)
>
> [5.1.1.4 繞路（Detour）： 204](#繞路detour)
>
> [5.1.1.5 群組（Group）： 204](#群組group-1)
>
> [5.1.1.5.1 基本概念 (Basic Concept)： 204](#基本概念-basic-concept)
>
> [5.1.1.5.2 群組設計原則 (Group Design Principle)： 204](#群組設計原則-group-design-principle)
>
> [5.1.1.5.3 群組重疊設定 (Group Overlap Configuration)： 205](#群組重疊設定-group-overlap-configuration)
>
> [5.1.1.6 車輛優先級(Priority)： 206](#車輛優先級priority)
>
> [5.1.1.7 單行道 (One-Way Path)： 207](#單行道-one-way-path)
>
> [5.1.1.8 逆向超車功能 (Reverse Overtaking)： 208](#逆向超車功能-reverse-overtaking)
>
> [5.1.1.9 路名設定 (Road)： 208](#路名設定-road)
>
> [5.1.2 交管設施（Traffic Control Facilities）： 210](#交管設施traffic-control-facilities)
>
> [5.1.2.1 路口點（Junction）： 210](#路口點junction-1)
>
> [5.1.2.2 交管點（Traffic Point）： 213](#交管點traffic-point)
>
> [5.1.2.3 待命點（Standby Station）： 213](#待命點standby-station-1)
>
> [5.1.2.4 臨停點 (Temporary Park Only)： 214](#臨停點-temporary-park-only)
>
> [5.1.2.5 尋找替代道路功能 (Find Way Time)： 214](#尋找替代道路功能-find-way-time)
>
> [5.1.2.6 取得路權超時功能 (GetRightTimeout)： 215](#取得路權超時功能-getrighttimeout)
>
> [5.1.2.7 手臂動作中鎖路權(RobotRouteLock)： 215](#手臂動作中鎖路權robotroutelock)
>
> [5.1.3 塞車解決方法（Traffic Jam Solutions）： 215](#塞車解決方法traffic-jam-solutions)
>
> [5.1.3.1 趕車（Vehicle Relocation）： 215](#趕車vehicle-relocation)
>
> [5.1.3.2 強制讓道功能 (Force Yielding)： 217](#強制讓道功能-force-yielding)
>
> [5.1.3.3 重繞路（Re-Detour）： 217](#重繞路re-detour)
>
> [5.1.3.4 路口避車（Intersection Avoidance）： 218](#路口避車intersection-avoidance)
>
> [5.1.3.5 調車（Vehicle Dispatch）： 218](#調車vehicle-dispatch)
>
> [5.1.3.5 指定避車點（Designated Avoidance Point）： 218](#指定避車點designated-avoidance-point)
>
> [5.1.3.6 狹小路段兩車交會（Narrow Lane Vehicle Passing）： 219](#狹小路段兩車交會narrow-lane-vehicle-passing)
>
> [5.2 搬運任務併車邏輯（Task Merging Logic） 221](#搬運任務併車邏輯task-merging-logic)
>
> [5.2.1 情境定義（Scenario Definition）： 221](#情境定義scenario-definition)
>
> [5.2.2 範例（Examples）： 221](#範例examples)
>
> [5.2.2.1 併車邏輯範例一、合併交換料任務（Merging Exchange Tasks）： 222](#併車邏輯範例一合併交換料任務merging-exchange-tasks)
>
> [5.2.2.2 併車邏輯範例二、合併上下料任務（Merging Loading and Unloading Tasks）： 223](#併車邏輯範例二合併上下料任務merging-loading-and-unloading-tasks)
>
> [5.2.2.3 併車邏輯範例三、合併交換料與上下料任務（ Merging Exchange and Loading/Unloading Tasks）： 224](#併車邏輯範例三合併交換料與上下料任務-merging-exchange-and-loadingunloading-tasks)
>
> [5.3 群組設計原則 ( Group Define ) 226](#群組設計原則-group-define)
>
> [5.3.1 群組設計的定義（Group Design Definition）： 226](#群組設計的定義group-design-definition)
>
> [5.3.2 自走車規格（AGV Specifications）： 226](#自走車規格agv-specifications)
>
> [5.3.3 群組設計（Group Design）： 226](#群組設計group-design)
>
> [5.3.3.1 基本規則第一點（Basic Rule 1）： 226](#基本規則第一點basic-rule-1)
>
> [5.3.3.2 基本規則第二點（Basic Rule 2）： 227](#基本規則第二點basic-rule-2)
>
> [5.3.3.3 基本規則第三點（Basic Rule 3）： 227](#基本規則第三點basic-rule-3)
>
> [5.3.3.4 基本規則第四點（Basic Rule 4）： 228](#基本規則第四點basic-rule-4)
>
> [5.3.3.5 特殊情境 1 - 路口點 (\*註1)（Special Scenario 1 - Junction）： 228](#特殊情境-1---路口點-註1special-scenario-1---junction)
>
> [5.3.3.6 特殊情境 2 - 雙線道（Special Scenario 2 - Dual Lane）： 229](#特殊情境-2---雙線道special-scenario-2---dual-lane)
>
> [5.4 Log 解讀 ( Log Interpretation ) 231](#log-解讀-log-interpretation)
>
> [5.4.1 收到移動路徑指令 (Receiving Movement Path Command)： 231](#收到移動路徑指令-receiving-movement-path-command)
>
> [5.4.1.1 Get move_control...： 231](#get-move_control...)
>
> [5.4.1.2 path: deque(\[\[...\], \[...\], ...\])： 231](#path-deque...-...-...)
>
> [5.4.1.3 get_right...： 232](#get_right...)
>
> [5.4.2 下達移動命令 (Issuing Movement Command)： 232](#下達移動命令-issuing-movement-command)
>
> [5.4.2.1 Get Lock： 232](#get-lock)
>
> [5.4.2.2 路權確認： 232](#路權確認)
>
> [5.4.2.3 move_cmd...： 233](#move_cmd...)
>
> [5.4.3 過站不停命令 (Pass-Through Command)： 233](#過站不停命令-pass-through-command)
>
> [5.4.4 路權管理 (Right-of-Way Management)： 234](#路權管理-right-of-way-management)
>
> [5.4.4.1 路權釋放的基礎：車輛位置回報 (Vehicle Position Reporting)： 234](#路權釋放的基礎車輛位置回報-vehicle-position-reporting)
>
> [5.4.4.2 路權釋放模式 (Right-of-Way Release Modes)： 234](#路權釋放模式-right-of-way-release-modes)
>
> [5.4.4.3 日誌中的路權資訊解讀 (Interpreting RoW Information in Logs)： 235](#日誌中的路權資訊解讀-interpreting-row-information-in-logs)
>
> [5.4.5 路權管理 (Right-of-Way Management)： 235](#路權管理-right-of-way-management-1)
>
> [5.4.5.1 抵達站點訊息 (Arrival Messages)︰ 235](#抵達站點訊息-arrival-messages)
>
> [5.4.5.2 路權釋放的判斷與日誌記錄 (RoW Release Logic and Logging)： 236](#路權釋放的判斷與日誌記錄-row-release-logic-and-logging)

# 

# 系統對應版本

TSC_v8.14B

## 版次更新紀錄

| 文件編號 | 軟體版本 | 修改內容 | 修改人 | 審核人 | 修改時間 |
|----|----|----|----|----|----|
| v2.0.0 | 待補 | 因應 Google 文件新版本功能以及 TSC UI 系統版本內容更新，文件重新規整。 | 郭書銘 |  | 2025年02月07日 |
| v2.0.1 | 待補 | 補充圖表狀態敘述與交管說明。 | 郭書銘 |  | 2025年04月22日 |
| v2.0.2 | 待補 | 補充 Point Property ( 4.10.3.16.9 )、Path Property (4.10.4.14) 說明。 | 郭書銘 |  | 2025年05月08日 |
| v2.0.3 | 待補 | 修正部份章節排版 | 郭書銘 |  | 2025年09月26日 |

**易捷系統股份有限公司 保留所有權利**

　　本手冊中所述的產品和規格可能會在未事先通知的情況下進行修改。

　　易捷系統股份有限公司 ( 以下簡稱易捷系統 ) ，擁有本產品及其軟體的專利權、版權和其他知識產權。如有客製化需求，請與我們的業務團隊聯繫。

　　歡迎閱讀 Transfer System Controller 系統 ( 以下簡稱 TSC 系統 ) 操作手冊。這份手冊將指導您使用 TSC 系統的功能。

　　如有任何問題或建議，請與我們的技術支援團隊聯繫。我們非常感謝您的反饋，以不斷改善我們的產品和服務。

# 1. 操作手冊主要內容

　　本手冊由三大部份組成：

1.  第一部份詳細介紹了 TSC 系統的功能、使用指南和項目名稱的命名規則。

2.  第二部份包含兩部分內容：面向操作人員的基礎功能使用說明，以及面向管理人員的進階功能使用說明。

3.  第三部份專注於使用注意事項、常見問題和解答，為您提供實用的指導和解決方案。

　　這份手冊旨在幫助您全面了解和操作 TSC 系統，並提供必要的資訊和指導。請按照章節順序閱讀，以獲得最佳的學習體驗。

# 2. 系統及基本功能介紹

## 2.1 使用環境與作業系統

1.  伺服器端：TSC 系統安裝在 Linux 系統上即可使用。由於不同的 Linux 發行版可能存在差異，本文將不詳細說明如何安裝 Linux 系統。請參考您使用的發行版的安裝教學和系統安裝文件。

2.  操作介面：建議使用 Windows 10/11 操作系統，以符合瀏覽器版本功能的需求。為了獲得最佳的使用體驗，我們建議您使用最新版本的 Google Chrome 瀏覽器。

## 2.2 硬體需求

1.  處理器：建議使用多核心處理器，以確保系統運行順暢。

2.  硬碟：一個 SSD 硬碟作為系統安裝碟。兩個 HDD 硬碟使用 Raid 1 方式進行資料保護。

3.  記憶體：由於使用 Google Chrome 瀏覽器，建議配備 16GB 記憶體，以獲得流暢的使用體驗。

4.  螢幕：建議使用 24 吋螢幕，以維持最佳的使用效果。解析度設定為 1920\*1080，100% 比例。

## 2.3 功能與特色說明

1.  網頁型式：TSC 系統採用網頁形式，通過瀏覽器即可使用，降低了初始使用門檻，無需複雜的安裝過程。

2.  易學易用：本操作手冊採用淺顯易懂的教學內容，搭配實際操作範例，適合初學者和有經驗的使用者。

3.  專案管理：TSC 系統採用專案管理觀念，以視覺化方式管理廠房設備，使數據圖像化，提高工作效率和可視性。

4.  提升效率：TSC 系統簡化了複雜的工作流程，通過直觀的操作界面和專案管理，幫助使用者快速完成任務，提升整體工作效率。

## 2.4 系統安裝

　　伺服器端的 TSC 系統安裝流程詳細寫於 TSC 安裝文件中。如果您需要了解安裝步驟，請先參閱該文件。後續我們將把該文件內容補充到本操作手冊中，以提供更全面的指導。

　　一旦伺服器安裝完畢並正式啟動，您可以取得伺服器 IP 地址。

　　在瀏覽器的網址列中輸入該 IP 地址，連接埠依現場設定，可能為 3000 PORT（即 3000 端口）或 80 PORT。

　　舉例來說，您可以輸入：192.168.0.64:3000 或 192.168.0.233。

![](media/image284.png)

> IP 地址需以現場實際狀況為主，內網管理和外網連接的 IP 地址可能不同。請與相關人員確認正確的 IP 地址。
>
> 為了獲得最佳的使用體驗，我們建議您使用 Google Chrome 瀏覽器作為首選。

![](media/image221.png)

## 2.5 相關文件

| 文件編號 | 參考手冊                       | 修改時間       |
|----------|--------------------------------|----------------|
| v1.0.3   | TSC 安裝手冊 Oracle Linux 初版 | 2024年08月02日 |
| ※ 註 1   | TSC SECS GEM Specification     |                |

※ 註 1：因現場使用規範不盡相同，請依現場使用規範向相關人員索取對應文件。

# 3. 開始使用TSC系統

　　在開始介紹系統內容之前，首先了解一下系統架構，請見下圖：

　　現有 TSC 系統不包含基本設定的導覽列，共有十七個功能頁面，各頁面分別代表不同階段的設定。

　　我們可以透過下方導覽圖了解，整體系統的運作流程：

　　現在可以初步了解 TSC 系統整體的設置流程，我們開始進行使用的第一步。

## 3.1 第一次使用，登入畫面

　　當您完成軟硬體安裝的前置作業後，使用管理人員提供的 IP 地址和連接埠，在瀏覽器中輸入，就會出現登入畫面。

![](media/image49.png)

　　輸入管理文件中提供的帳號和密碼，點擊登入按鈕，即可進入 TSC 系統的主看板。

　　※ Rememeber Me：勾選此選項後，您的登入帳號將被暫存，避免在以下兩種情況下需要重新登入：

1.  不關閉瀏覽器但關閉該分頁並重新開啟。

2.  同時開啟多個分頁時。

　　注意：如果完全關閉瀏覽器，您將需要重新登入。

　　最高管理員帳號：開放所有頁面與功能。

　　唯讀帳號：僅查看部份頁面與功能。

![](media/image13.png)

IP 與連接埠：

　　IP 地址為 192.168.0.168，連接埠為 3000。輸入該 IP 地址後，瀏覽器會自動導向登入畫面，網址為 192.168.0.168:3000/login。

　　輸入帳號和密碼進行登入。此處示範使用 admin 帳號，實際使用時請按照現場人員提供的對應權限帳號進行登入。

![](media/image165.png)　　![](media/image348.png)

　　　　　　　登入畫面示意圖　　　　　　　　　　　帳號密碼錯誤會進行提示

![](media/image308.png)

登入成功會直接進入主看板，請見接下來的章節。

## 3.2 主看板

　　登入系統後，您將進入主看板。剛安裝完畢的主看板通常非常簡潔，這時您需要新增專案內容來填充它。

![](media/image138.png)

　　隨著您逐步完成專案設定，主看板上的功能會逐漸增加。這些功能項目可能會因現場設備的不同而略有差異，但基本內容是相似的。

![](media/image182.png)

　　通常，現場人員會在安裝過程中建立該專案所包含的專案內容，或安裝內建的預設專案。因此，您不必擔心主看板的初始狀態。請放心，我們會一步一步地帶領您探索 TSC 系統的各項操作和功能。

　　從設定完成圖中我們可以發現，TSC 系統的介面布局可分為下圖幾個區塊：

![](media/image387.png)

　　基本上各頁面布局不會差太多，降低學習成本。

　　我們接下來會開始進入大章節，介紹各頁面的內容。

# 4. 系統介面說明

　　這個章節開始，我們會針對每個頁面的結構與內容，還有系統規則進行說明。

　　雖然會有部分重覆，但這是加深印象的幫助，尤其在系統內容較多且複雜的情況下。

　　TSC 系統 目前有上圖表上的這些頁面，可能會依功能進行調整，但大體上是差不多的。

　　我們直接從 主看板（Dashboard） 開始進行說明。

## 4.1 主看板 ( Dashboard )

　　登入正常運行的系統時，進入首頁，可以看見與下圖相似的畫面。

![](media/image149.png)

　　因現場設備設定狀況，所顯示的資訊可能略有差異。

　　尚未設定資料時，該欄位可能不顯示，此部分可詢問相關人員。

### 4.1.1 導覽列

| Dashboard               | 主看板         |
|-------------------------|----------------|
| 　-　Workstations       | 工作站管理     |
| Zone Management         | 區域管理       |
| Transfer Statistics     | 搬運統計管理   |
| 　-　Vehicle Statistics | 自走車統計管理 |
| 　-　Commands           | 命令歷史紀錄   |
| Transfer Dashboard      | 搬運任務看板   |
| Map Management          | 地圖管理       |
| 　-　Map Editor         | 地圖編輯       |
| Vehicle Dashboard       | 自走車看板     |
| 　-　Vehicle Management | 自走車管理     |
| eRack Dashboard         | 電子貨架看板   |
| 　-　eRack Management   | 電子貨架管理   |
| IOT Device Management   | 物聯網設備管理 |
| Components Maintain     | 設備維護       |
| Account Management      | 帳號管理       |
| Log Management          | 系統紀錄管理   |
| Log Files               | 系統紀錄檔管理 |

### 4.1.2 功能列

![](media/image366.png)

#### 4.1.2.1 導覽列最大化最小化按鈕

> 用於調整左側導覽列的顯示大小。

#### 4.1.2.2 專案功能選單

> 下拉式選單，點擊可進行新增、打開、編輯專案。
>
> ![](media/image278.png)

##### 4.1.2.2.A 新增專案 ( New Project )

> 用於創建新的專案。

![](media/image180.png)

![](media/image284.png)

　　專案名稱（Project Name）：

　　為維持系統正常運作，專案名稱切勿以數字開頭、勿含空格、勿以純數字為名，勿輸入中文。

![](media/image221.png)

　　※ 具體命名請與相關人員討論：專案名稱的具體命名規則，請與相關人員討論確認。

　　使用系統（System Usage）：一般為兩者皆勾選。

##### 4.1.2.2.B 選擇專案 ( Select Project )

##### ![](media/image383.png)

可選擇系統內現有專案進行切換。

##### 4.1.2.2.C 編輯專案 ( Edit Project )

##### ![](media/image329.png)

> 顯示編輯該專案名稱與設定，目前無法進行變更。
>
> 如要更改專案檔案名稱，請見下方 另存專案（Save As Project）。

##### 4.1.2.2.D 匯出專案 ( Export Project )

![](media/image258.png)

點擊匯出後將有複數檔案進行下載，一般來說瀏覽器會請求確認允許下載，請點擊允許，此時會有六個檔案陸續要求下載。

![](media/image146.png)

##### 4.1.2.2.E 匯入專案 ( Import Project )

> 如果執行過匯出的話，此時就可以理解在匯入時為什麼會有那麼多項目需要選擇，務必確認獲得的專案檔案是否一致，否則將會匯入失敗。

![](media/image112.png)

![](media/image284.png)

　　為了方便專案（Project）的高移植性，並且提升人員測試的便利性，新增 匯出（Export） 及 匯入（Import） 功能。

　　匯出（Export） 可將當前專案的所有內容匯出，包含地圖資料、MR、eRack、IOT 裝置、區域（Zone）等設定。

　　只要將這些檔案提供給其他人，便可在其他台 TSC 系統 上馬上重現現場專案。

**　　匯入（Import） 及 匯出（Export） 的 UI 版本需相同才能成功匯入。**

**　　若版本有差異，可能無法成功匯入，需與相關人員確認。**

![](media/image221.png)

#### 4.1.2.3 專案名稱 (Project Name)

![](media/image317.png)

可清楚了解當前專案與相關專案檔案名稱。

#### 4.1.2.4 淺色模式與深色模式（Light Mode and Dark Mode）

![](media/image405.png)

> 系統提供淺色模式與深色模式的切換功能，使用者可依個人喜好或環境需求調整介面顯示風格。

#### 4.1.2.5 語言切換（Language Switch）

![](media/image434.png)

> 可切換成 繁體中文（Traditional Chinese）、簡體中文（Simplified Chinese）、英文（English）。

#### 4.1.2.6 警告訊息通知（Warning Message Notification）

![](media/image341.png)

> 點擊會跳轉至 警告訊息列表頁（Warning Message List Page），內含報錯資訊，為判斷錯誤訊息來源之一。

#### 4.1.2.7 登入狀態（Login Status）

> 登入後會出現部分操作項目，並顯示目前登入的管理帳號為何。

![](media/image50.png)

> 點擊帳號後，管理員選單（Users）會有下方兩個選項：
>
> 我的帳號（My Account）： 可進入帳號管理頁面，詳見 『帳號管理（Account Management）』。
>
> 登出（Logout）： 可直接登出帳號。

#### 4.1.2.8 基本設定圖示（Basic Settings Icon）

> 齒輪圖示，點擊後會打開側邊欄位選項，因屬重要項目故獨立取出，詳見欄目 『4.2 基本設定（Basic Settings）』。

### 4.1.3 主看板內容資訊

### ![](media/image399.png)

#### 4.1.3.1 自走車狀態（AMR Status）：

![](media/image20.png)

　　我們把相關區塊局部放大，這裡有兩個部分可以進行點擊：

　　點擊位置Ａ：

![](media/image198.png)

　　　　會出現彈跳視窗選項，主要是呈現該自走車的警告提示。

　　　　如果出現相關問題，可以知道車輛問題出在哪裡。

　　　　點擊 Reset 可以重新設定載具的初始狀態。

　　點擊位置Ｂ：

　　　　則會下拉顯示詳細的自走車資訊，依序是自走車的目前狀態、所在位置、訊息、備註。

　　　　None 中的內容是一般是顯示自走車使用的系統版本，這裡是模擬自走車，所以沒有版本號可以顯示。

![](media/image284.png)

　　 自走車狀態為 Unassigned 才可接受指令。

　　狀態種類共有十五種，因項目內容較多，詳細說明請至 『4.11.6.2 自走車狀態列表 ( Vehicle Status List)』 進行所有參數的了解。

![](media/image221.png)

#### 4.1.3.2 工作站狀態（Workstations Status）：

　　此欄位須開啟 TSC 設定 中的 EAPConnect 才會顯示，因此沒有使用這兩個功能的專案將不會顯示此欄位。

![](media/image370.png)

　　位置Ａ的欄位依序為『機台設備名稱』、『機台設備狀態』、『自走車ID』，『機台設備名稱』的命名規則可至『工作站管理』頁面進行了解。

　　位置Ｂ可以進行點擊，切換該機台狀態，點擊後打開如下圖的彈跳視窗，可以變更機台設備的狀態或把狀態重置。

![](media/image339.png)

目前『自走車狀態』共有四種：

| <span class="mark">Loaded</span>   | <span class="mark">已上貨</span>     |
|------------------------------------|--------------------------------------|
| <span class="mark">UnLoaded</span> | <span class="mark">已下貨</span>     |
| <span class="mark">Running</span>  | <span class="mark">機台運作中</span> |
| <span class="mark">AGVDone</span>  | <span class="mark">暫無效果</span>   |

#### 4.1.3.3 電子貨架狀態（Erack Status）：

![](media/image139.png)

　　主要顯示與當下專案串聯的 電子貨架（eRack），標示出 電子貨架 ID（eRack ID） 與電子貨架中的欄位狀態。

顏色狀態代表資訊：

| ![](media/image186.png) | ![](media/image31.png) |
|----|----|
| 灰色：儲位為空的。 | 藍色：儲位有讀到FOUP ID。 |
| ![](media/image212.png) | ![](media/image192.png) |
| 淺綠色：儲位有讀到 FOUP ID，MES 有回傳資訊。 | 紫色：儲位被 MR 預訂，MR 會對此儲位上下貨。 |
| ![](media/image277.png) | ![](media/image243.png) |
| 黃色：儲位上有異物。 | 紅色：未連線。 |

　　因內容繁雜，電子貨架的狀態詳細說明請見 『電子貨架看板（eRack Dashboard）』 頁面。

#### 4.1.3.4 版本與改版資訊（Version and Changelog Information）：

![](media/image398.png)

　　頁面下方皆有版本相關資訊，若遇到操作手冊說明或故障排除無法解決的事項時，可告知相關人員版本號及系統異常紀錄。

　　滑鼠移到版本號上，會有滑過效果，可點擊對應的版本號進入 『改版紀錄（Changelog）』 查看改版資訊。

![](media/image331.png)![](media/image345.png)

　　　　　UI Changelog　　　　　　　　　　　　　　　TSC Changelog

## 4.2 基本設定 ( Settings )

　　因此項目設定繁雜，內容較多，故成獨立項目，一般較少對此進行設置。

　　從 『4.1 主看板（Dashboard）』 可以知道，點擊齒輪選項後會出現右側選單，右側選單可分為兩個區塊：

1.  管理員資訊（Admin Information）

2.  TSC 系統設定（TSC System Settings）

![](media/image284.png)

**　　如果需要使用此處的編輯選項，請先至 自走車看板（Vehicle Dashboard） 的位置，將 TSC 系統 暫停。**

![](media/image74.png)

　　暫停後，方可進行設定變更，修改完畢請記得回到此處啟用 TSC 系統。

![](media/image221.png)

### 4.2.1 管理員資訊

　　若下方設定變更，此區會出現設定按鈕，待所有選項確定後點擊設定按鈕進行變更套用。

　　

![](media/image181.png)　　![](media/image23.png)

　　　　一般狀態 　　　　　　　 設定修改後出現套用按鈕

###  

### 4.2.2 TSC 系統設定

　　設定 TSC 系統 各項參數，包含 RTD MODE、MR 安全設定、交通、充電 等設定。

| ![](media/image69.png) | 禁止編輯符號，如看見此符號，則代表未將 TSC 系統 暫停，請至 自走車看板（Vehicle Dashboard） 將 TSC 系統 暫停後，再進行修改。 |
|----|----|

#### 4.2.2.1 命令檢查 ( Command Check )：

#### ![](media/image372.png)

##### 4.2.2.1.1 白名單 ( CarrierWhiteMask )

　　勾選此項目，搬運命令中，若有存在白名單中的 Carrier，該搬運命令可被運送。若為名單之外的 Carrier，該搬運命令會被駁回，顯示 警示（Alarm）。

##### 4.2.2.1.2 等待佇列檢查（CarrierDuplicatedInWaitingQueueCheck）：

　　勾選此項目，批次命令的 等待佇列（Waiting Queue） 中，若有重複的 Carrier ID，該搬運命令會被駁回，顯示 警示（Alarm）。

##### 4.2.2.1.3 執行佇列檢查（CarrierDuplicatedInExcutingQueueCheck）：

　　勾選此項目，批次命令的 執行佇列（Execution Queue） 中，若有重複的 Carrier ID，該搬運命令會被駁回，顯示 警示（Alarm）。

4.2.2.1.4 來源地重複檢查（SourcePortDuplicatedCheck）：

　　勾選此項目，搬運過程中，來源地已有重複的 Carrier ID，該搬運命令會被駁回，顯示 警示（Alarm）。

##### 4.2.4.1.5 目的地儲位檢查（DestPortDuplicatedCheck）：

　　勾選此項目，搬運過程中，若目的地已有重複的 Carrier ID，該搬運命令會被駁回，顯示 警示（Alarm）。

##### 4.2.4.1.6 關聯 Carrier ID 檢查（AssociateCarrierIDCheck）：

　　勾選此項目，搬運過程中，若目的地已有重複的 Carrier ID，該搬運命令會被駁回，顯示 警示（Alarm）。

##### 4.2.4.1.7 啟用自動分配目標儲位（AutoAssignDestPortEnable）：

　　自走車從機台下貨時，由 ACS 自動選擇放置的目的地使用，**目前已無作用**。

![](media/image13.png)

　　 功能說明：

　　這裡說明 TSC 系統 在分配搬運任務命令時，關於辨識 目的地（Destination） 的設定規則。

　　如果今天目的地的位置設定為 『＊』 或 『E0P0』 時，TSC 系統 會針對此項任務指令的 『來源位置（Source）』 中去尋找。

**※ 來源位置在機台（Workstations）的範例：**

　　搬運任務命令如下時

![](media/image35.png)

　　系統會去尋找 GY001 的所在位置，例如所在位置在編號 WSD158 的製程機台上，系統會從機台設定內的『Return To』去尋找。

　　機台 WSD158 的 Return To 為 E002，也就是編號 E002 的電子貨架。此時系統會從電子貨架 E002 中尋找空儲位，讓自走車將 GY001 遞送過去。

![](media/image385.png)

**※ 來源位置在電子貨架 ( Eracks ) 的範例：**

　　搬運任務命令如下時

![](media/image59.png)

　　系統會去尋找 GY005 的所在位置，例如所在位置為編號 E001 的電子貨架的儲位 E1P5 上，則此筆命令會在電子貨架 E001 的儲位中，尋找一個位置放上。

![](media/image220.png)

　　也就是說，假設整個電子貨架 E001 只有儲位 E1P5 上的載具 GY005 時，發送此命令，會將 GY005 送至 E1P1 上。

![](media/image308.png)

　　除了選擇『＊』跟『E0P0』外，可代入加上的選項為：

| 電子貨架的 Zone ID，例：zone1\*  | 電子貨架的 Group ID，例：G001\*   |
|----------------------------------|-----------------------------------|
| 電子貨架的 Device ID，例：E001\* | 儲位的 Area 名稱，例：ER_WaitIn\* |

　　在各類別項目後面加上『＊』，各類別命名規則請依公司管理方法進行規劃。

　　這些選項的會有順序的層級關係，層級關係為：

![](media/image259.png)

　　若指令屬於左側範疇，目的地電子貨架若沒位置會向上層尋找，朝同群組的電子貨架去尋找空儲位，同群組沒有就再向上往同區域去尋找。

　　Area ID 獨立出來是因為它可能跨區、跨群組、跨電子貨架，如果在其中沒找到空儲位則直接發出警示提醒相關人員進行處理。

- AverageErackCapacityEnable

![](media/image371.png)

　　勾選啟用後，系統會平均分配群組中的貨架水位，使每個貨架的水位相同。

- ReturnToFirst

![](media/image106.png)

　　勾選啟用後，系統會以該貨架的第一個儲位為主，並依序進行擺放。

- AllowBackwardSearchEnable

![](media/image38.png)

　　勾選啟用後，會出現兩個選項，系統會允許向上層級尋找空儲位，未勾選就依原先指定目的範圍尋找。向上選項主要以 Groups 跟 Zones 為主。

![](media/image13.png)

　　各項目所代表的設計原則我們這裡用下圖來解說，下圖應為一排電子貨架，但圖片較長不易看，故此處依群組分開。

![](media/image102.png)

　　假設今天我們有三座 4\*4 的電子貨架，Rack ID 分別是 E001、E002、E003，將 E001 跟 E002 組成群組 Z001，E003 自己為一群組 Z002，總計為 48 個儲位。

　　當我們想把電子貨架依需求分配進行貨物儲放的動作時，如何將特定數量的欄位分給指定的功用呢？我們可以先到『電子貨架管理』去新增 Sector ID，如圖中可以發現我們需要的有三種，『WAIT_IN』、『WAIT_OUT』、『NG_PORTS』，具體使用與命名可以自行討論。

　　所以我們把這三種先加到 Sector 裡面。![](media/image158.png)

　　新增完畢後，前往『電子貨架管理』把想要新增的部分加上。點開電子貨架的編輯按鈕，出現編輯視窗，或是新增新的電子貨架時，找到 Sector 欄位直接加上。

![](media/image250.png)

　　填寫內容是Sector ID加上我們想加在裡面的欄位號碼。

　　範例：{"Sector ID":"1,2,3,4,5,6,7,8,9,10,11,12"}

　　如此一來，結果就會同下圖在『電子貨架看板』，全部被區分在一個 Sector 中。

![](media/image129.png)

　　我們回到範例最初的參考圖，直接使用 E002 做為例子，因為它正好處於中間比較複雜的位置。

![](media/image344.png)

　　E002 Sector 欄位內容，Sector 與 Sector 之間請用逗號隔開：

　　{"WAIT_IN":"1,2,5,6","WAIT_OUT":"3,4,7,8","NG_PORTS":"9,10,11,12"}

　　設定完後我們到『電子貨架看板』，可以看到設定結果。

　　系統會統合所有相同的 Sector ID ，將它匯整為 Area ID，所以不用擔心跨貨架的問題，相對來說，做好妥善的儲位規劃是很重要的。

　　以上是針對 Group ID、Area ID、Sector ID、Rack ID 的綜合範例說明，搭配

AutoAssignDestErackPortBy 的設定，可針對特定儲位進行平均分配儲存，不知道這樣是否有比較清楚了？仍有疑問的話，可詢問相關人員。

![](media/image308.png)

#### 4.2.2.2 命令調度 ( Command Dispatch )：

##### ![](media/image403.png)

##### 4.2.4.2.1 DivideDispatchZoneEnable ( 依區域分割調度 )

　　勾選此項目後，自走車會依分配的區域進行指令分割調度。

##### 4.2.4.2.2 DivideMethodByMachinePior ( 依指令分割的設定進行調度安排 )

　　此項目設定選擇為下拉選單，選取指令分割的方式。

　　DivideMethod ( 分割調度的方式 )

　　　　 - BySourePort

　　　　　　從來源儲位進行分配。

　　　　 - ByDestPort

　　　　　　從目的地儲位進行分配。

#### 4.2.2.3 晶圓盒規格感測 ( Cassette Type Sensitive )：

![](media/image26.png)

##### 4.2.2.3.1 晶圓盒規格感測啟用（CassetteTypeSensitiveEnable）：

　　勾選後啟用晶圓盒規格感測功能。

![](media/image123.png)

##### 4.2.2.3.2 晶圓盒規格感測方法（CassetteTypeSensitiveMethod）：

從載具 ID 判斷（ByCarrierID）：

　　選擇此項目，若載具 ID 中帶有相關參數，則可判斷晶圓盒是哪種規格。

從搬運命令判斷（ByTransferCmd）：

　　選擇此項目，若搬運命令中帶有相關參數，則可判斷晶圓盒是哪種規格。

載具類型前綴（CassetteTypePrefix）：

　　可設定載具尺寸前綴供系統判斷，預設為 12S（12吋） 與 8S（8吋）。

##### 4.2.2.3.3 電子貨架晶圓盒類型檢查（ErackCassetteTypeCheck）：

　　若開啟的話，則會檢查 source 及 dest 是否為 erack，是的話則會檢查指令的 carrier type 是否有符合 erack 上的設定。

#### 4.2.2.4 保護機制 ( Safty )：

![](media/image108.png)

##### 4.2.2.4.1 電子貨架狀態檢查（ErackStatusCheck）：

　　電子貨架上儲位狀態檢查，檢查有無物料和 Carrier ID 的狀態資訊是否滿足當下的上下貨動作。

##### 4.2.2.4.2 儲位狀態檢查（BufferStatusCheck）：

　　電子貨架、自走車上儲位狀態檢查，檢查有無物料，和 載具 ID 是否滿足當下的上下貨動作。

##### 4.2.2.4.3 預綁定檢查（PreBindCheck）：

　　當開啟該功能，自走車於工作站中取完貨後，會比對指令的 carrierID 及自走車讀取到的 carrierID，若比對失敗則會進入嚴重錯誤 ( Serious Alarm)（需人員介入）。

##### 4.2.2.4.4 重命名失敗 ID（RenameFailedID）：

　　開啟時，若自走車 回報讀取錯誤 ( Readfail )，TSC 則會將指令的 carrierID 強制寫入自走車中（僅測試及特殊場域使用）。

##### 4.2.2.4.5 儲位位置檢查（BufferPosCheck）：

　　當自走車不是處在手臂動作及暫停 ( Pause ) 狀態下，若自走車回報儲位 ( Buffer )上位置錯誤 ( Position Error ) 時，TSC 會有一個警告 ( Warning ) 訊息，但若開啟該設定則會進入暫停 ( Pause ) 狀態。

##### 4.2.2.4.6 取消儲位 RFID 檢查（BufferNoRFIDCheck）：

　　取消檢查自走車儲位上 RFID 狀態（有操作風險，僅作運行測試用）。

##### 4.2.2.4.7 來源位置不符檢查（SourceLocationMismatchCheck）：

　　當 TSC 收到指令並檢查完成後，指令會在等待佇列 ( waiting queue ) 中等待派給自走車。

　　當要配給自走車時，若指令有帶 carrierID，則 TSC 會在系統中找尋這個 carrierID 的實際位置。

　　若有找到並且實際位置與指令位置不一致時，則會將指令的來源 ( Source ) 改為實際位置。

　　若開啟該選項則不會修改，並且觸發 告 ( Warning ) 訊息提示。

##### 4.2.2.4.8 跳過上貨中止時的下貨中止（SkipAbortLoadWhenUnloadAbort）：

　　針對同一個裝卸口 ( Loadport ) 的上下料指令，TSC 會自動將其連結 ( Link ) 起來使其變成一組交換貨指令。

　　由於安全起見，當下貨指令失敗時會同步將上貨指令刪除。

　　但若開啟該設定，則中止 ( Abort ) 時不會自動刪除。

4.2.2.4.9 跳過上貨取消時的下貨取消（SkipCancelLoadWhenUnloadCancel）：

　　針對同一裝卸口 ( Loadport ) 的上下料指令，TSC 會自動將其連結 ( Link ) 起來使其變成一組交換貨指令。

　　由於安全起見，當下貨指令失敗時會同步將上貨指令刪除。

　　但若開啟該設定，則取消 ( Cancel ) 時不會自動刪除。

##### 4.2.2.4.10 斷開時釋放路權（ReleaseRightWhenDisconnected）：

　　當異常發生時，勾選該選項則會釋放路權。

##### 4.2.2.4.11 搬運位移檢查（TrShiftReqCheck）：

　　當來源點 ( Source ) 及 目標點 ( Dest ) 為同一個點上時，自走車可以直接進行 A to B 的搬運，不需要先搬至自走車身上（該功能尚在開發中，並且需與相關人員確認）。

##### 4.2.2.4.12 省略搬運上架檢查（SkipTrLoadReqWhenSwapTask）：

　　在執行交換任務時，跳過向上位系統確認的步驟。

　　應用情境為執行交換任務時，當貨物被取下，表示機台或貨架上該儲位肯定為空，可跳過向上位系統確認是否上貨的步驟。

##### 4.2.2.4.13 搬運上架檢查（TrLoadReqCheck）：

　　自走車到工作站準備上貨前，向上位系統確認能否上貨，允許後，手臂才會從自走車的儲位下貨，上到工作站的儲位上。

##### 4.2.2.4.14 搬運上架檢查逾時設定（TrLoadReqTimeout）：

　　等待上位系統確認上貨，超過多久發生警示。

##### 4.2.2.4.15 搬運下架檢查（TrUnloadReqCheck）：

　　自走車行走到工作站準備下貨前，向上位系統確認能否下貨，允許後，手臂才會從工作站的儲位搬貨到自走車的儲位上。

##### 4.2.2.4.16 回傳檢查（TrBackReqCheck）：

　　開啟該選項的話，當自走車於 Gyro 的電子貨架上貨時，當貨物放好時，會先確認 電子貨架上回傳資訊，確認後才將手臂伸回（特殊運用，請先與相關人員確認）。

##### 4.2.2.4.17 設備回傳檢查（TrBackReqCheckForEQ）：

　　開啟該選項的話，當自走車於設備 ( Equipment )上貨時，當貨物放好時，會發送一個 事件 ( Event ) 給上位系統，待上位系統回覆後才將手臂伸回（特殊運用，請先與相關人員確認）。

##### 4.2.2.4.18 回傳檢查逾時設定（TrBackReqTimeout）：

　　等待手臂伸回的時間。

##### 4.2.2.4.19 交換任務逾時設定（TrSwapReqTimeout）：

　　設定交換任務的逾時時間，暫無用途。

#### 4.2.2.5 批次任務設定 ( Batch Run )：**(目前已無作用)**

![](media/image368.png)

##### 4.2.2.5.1 批次命令大小（Batch Size）：

　　設定車輛執行批次搬移命令的數量，最多設定為 6，即三組命令。

　　例：batch size:4，表示執行 4 個 single transfers 或 2 個 replace transfers。

##### 4.2.2.5.2 收集命令逾時（Collect Timeout）（單位：秒）：

　　收集批次命令的區間結束時間。

##### 4.2.2.5.3 合併命令起始逾時（Merge Start Timeout）（單位：秒）：

　　第一筆命令在收集批次命令的追加等待時間。

　　運作邏輯：

　　一開始第一筆命令的總時間為：Merge Start Timeout + Collect Timeout。

　　當獲取第一筆命令後，後續命令的等待時間皆為 Collect Timeout，直到沒有命令，或是滿足 Batch Size 的命令數量時，則會進行任務發布。

#### 4.2.2.6 失敗復原設定 ( Recovery )：

![](media/image340.png)

##### 4.2.2.6.1 自動（Auto）：

　　如批次任務執行完，仍有殘貨，會自動清貨到自走車設定的指定電子貨架上。

##### 4.2.2.6.2 保留載具於車輛上（KeepCarrierOnTheVehicle）：

　　該選項位於 Auto 下方，由於開啟 Auto 時會自動釋放 Error 以下層級的 Alarm，並且檢查身上是否有殘貨，若有的話則會搬回指定貨架。

　　若只希望釋放 Alarm，但不希望處理殘貨的話，可勾選該選項。

##### 4.2.2.6.3 異常貨架載具類型檢查（FaultyErackCarrierTypeCheck）：

　　勾選該選項的話，則會透過之前的搬運指令來推算身上殘貨的 Carrier Type，當要執行殘貨處理時，則會確認目的地貨架是否支援該 Carrier Type。

##### 4.2.2.6.4 與自走車同步重置（ResetSyncWithMR）：

　　勾選該選項時，AMR 只要進行重新設定，系統將會同步進行重設。

##### 4.2.2.6.5 剩餘殘貨退回至（ResidualReturnTo）：

　　此項目為下拉選單：

![](media/image203.png)

> DefaultErack： 將殘貨送回該筆命令的貨物預設位置，從來源或目的地尋找可存放儲位，將殘貨送至該位置。
>
> FaultErack： 將殘貨送回自走車上所設定的 FaultErack 位置。

##### 4.2.2.6.6 發生錯誤警示時取消所有命令（AbortAllCommandsWhenErrorAlarm）：

　　當發生 Error 等級的 Alarm 時，會刪除身上所有指令。

##### 4.2.2.6.7 重大錯誤拒絕接收命令（AbortAllCommandsWhenSeriousAlarm）：

　　發生重大錯誤時，系統將會取消所有命令。

##### 4.2.2.6.8 發生錯誤警示時取消連結命令（AbortLinkCommandWhenErrorAlarm）：

　　無功能。

##### 4.2.2.6.9 重新分配目的地（ReAssignErackDestPortWhenOccupied）：

　　當目的地儲位被佔用時，重新分配電子貨架配送的位置。

　　例：當自走車執行搬運任務至目的地後，發現該儲位已被其他自走車擺上貨物時，若勾選此選項，自走車將會再次從目的地尋找可上貨的空儲位。

##### 4.2.2.6.10 移動重試（RetryMoveWhenAlarmReset）：

　　當警示重設後，重新嘗試移動。

##### 4.2.2.6.11 塞車重試（RetryBackThenForwardWhenJam）：

　　當塞車時，移動位置後重新嘗試前往目的地。

##### 4.2.2.6.12 無有效儲位時返回異常貨架（ReturnToFaultyErackWhenNoValidBuf）：

　　當發生與 Buffer 有關的 Alarm（Alarm Code:10018）時，開啟該功能可以重置 Alarm。

##### 4.2.2.6.13 下貨檢查失敗時重試（RetryWhenTrUnloadCheckNG）：

　　無功能。

#### 4.2.2.7 交通管制設定 ( Traffic Control )：

![](media/image162.png)

##### 4.2.2.7.1 啟用路口交管功能（Enable Traffic Point）：

　　是否使用路口交管功能。

##### 4.2.2.7.2 自動尋找路徑（Enable Find Way）：

　　是否自動尋找新的路徑（被自走車擋住的話）。

##### 4.2.2.7.3 優先選擇直行路線（EnableStraightRoadFirst）：

　　選擇行進路線的演算法會改為優先選擇同一路名的路線（地圖設定中的路線上可以設定路名）。

##### 4.2.2.7.4 行進角度固定（Keep Angle）：

　　保持固定角度進行移動。

##### 4.2.2.7.5 路權獲取逾時（Get Right Timeout）：

　　超過多久未獲取路權發生警報。

##### 4.2.2.7.6 路權獲取逾時重新尋路（Find Way Time）：

　　未獲取路權多久後會尋找新的路徑。

##### 4.2.2.7.7 最大繞路距離（Max Find Way Cost）：

　　繞路最大距離限制，單位為公尺。

##### 4.2.2.7.8 安全距離（Near Distance）：

　　單位為公釐（mm），為最近距離設定。

##### 4.2.2.7.9 持續行進範圍（KeepGoingRange）：

當 MR 距離路線中的 junction 還有多遠時，開始計算下一段路徑。

##### 4.2.2.7.10 動態釋放路權（Dynamic Release Right）：

　　動態釋放路權（到站釋放）。

##### 4.2.2.7.11 路權釋放來源（Release Right Based On Location）：

　　勾選時：透過 TSC 系統 目前路線的點位進行動態釋放路權的計算。

　　未勾選時：透過 MR 給的位置進行動態釋放路權的計算。

#### 4.2.2.8 通訊設定 ( Communication )：

![](media/image321.png)

##### 4.2.2.8.1 PS 協定（PS Protocol）：

　　與自走車的通訊協定。

##### 4.2.2.8.2 主機協定（Host Protocol）：

　　與上位系統的通訊協定。

##### 4.2.2.8.3 貨架命名規則（Rack Naming）：

　　設定電子貨架的命名格式，確保系統能正確識別與管理貨架。

![](media/image284.png)

　　 此設定因與其他系統串聯，無特別需求請勿更改其內容，在安裝時皆已設定完畢。 ![](media/image221.png)

#### 4.2.2.9 其他項目 ( Other )：

![](media/image140.png)

##### 4.2.2.9.1 從出發位置回報（ReportFromPortWhenVehicleDeparted）：

　　TSC 有一 E82 event VehicleDeparted，告訴上位系統從哪個位置出發，勾選後則會是告訴上位系統要去哪裡。

##### 4.2.2.9.2 啟用 SRTD 功能（SRTD Enable）：

　　是否開啟 Gyro 的 SRTD 功能。

##### 4.2.2.9.3 啟用 Stage 指令（Stage Enable）：

　　是否使用 stage 指令（特殊需求，需先諮詢相關人員）。

##### 4.2.2.9.4 支援 Loadport（Loadport Support）：

　　無功能。

##### 4.2.2.9.5 預先搬貨指令（PreDispatch）：

　　是否開啟預搬貨指令。

##### 4.2.2.9.6 針對電子貨架執行預先搬貨指令（PreDispatchForRack）：

　　是否針對 erack 執行預先搬貨指令。

##### 4.2.2.9.7 立即指派請求（ImmediatelyAssignedReq）：

　　當自走車開啟 predispatch 指令時，於 stock 前取完貨，會在原地等待後續是否有新的指令可以接。

　　若開啟該設定，則 TSC 會詢問上位系統後續是否還有其他指令，若沒有的話則可馬上出發，不需要浪費時間等待（特殊需求，需先諮詢相關人員）。

##### 4.2.2.9.8 啟用站點順序（StationOrderEnable）：

　　保留。

##### 4.2.2.9.9 跨區域中繼搬運（RelayTransferWhenCrossZone）：

　　無功能。

##### 4.2.2.9.10 自動清除預訂狀態（AutoResetBooked）：

　　當指令完成後，自動清除貨架上的 Booked 狀態（僅供測試，現場勿用）。

##### 4.2.2.9.11 延遲預訂（BookLater）：

　　正常情況下，當 TSC 收到指令時即會檢查貨架上是否可以放貨，若可以的話則會將該儲位 Booked 住，避免重複放置。

　　開啟該設定後，則是要 dispatch 時才會檢查（特殊需求，需先諮詢相關人員）。

##### 4.2.2.9.12 依需求中斷任務（WithdrawJobOnDemand）：

　　當 MR 處在沒任務的移動狀態下（例如 idle 充電、返回 standby 站等等），如果 waiting queue 中有可執行的指令，則可以讓 MR 停下原本的移動，並接受指令（特殊需求，需先諮詢相關人員）。

##### 4.2.2.9.13 停用 Port2Addr 對照表（DisablePort2AddrTable）：

　　是否使用新版手臂指令，舊版為 MR 身上會建立一個 port2address 的對照表。

　　當 TSC 下指令時，MR 透過對照表去執行對應手臂動作。

　　新版的則是透過 TSC 地圖上的點位設定，直接將參數送給 MR（新舊版 MR 設定會不一樣，須先與 MR 人員確認使用何種指令）。

##### 4.2.2.9.14 E84 連續取放功能（E84Continue）：

　　開啟時，當兩次指令的目標是一樣的話，可以透過 E84 連續取放的功能下達指令（1. 需使用新版手臂指令，2. 需與相關人員確認 MR 及機台是否支援）。

##### 4.2.2.9.15 EAP 連接（EAPConnect）：

　　開啟時會建立相關 workstation 程序，並且會於 UI 上顯示。

## 4.3 工作站( Workstation )

　　『工作站管理頁面（Workstation Management）』 為專案使用的製程設定，相關硬體設備建檔所使用。

　　透過此處設定，自走車方能與現場設備進行資訊串聯，才知道該到哪個任務安排的製程進行作業處理。

![](media/image346.png)

### 4.3.1 匯入工作站（Import Floor Workstations）：

　　點擊按鈕，打開匯入頁面。

![](media/image91.png)

![](media/image343.png)

　　Excel 範例檔截圖如下：

![](media/image422.png)

　　Excel 欄位格式：

| Floor, Row, Column, Device_ID, Equipment_ID, Equipment_State, Zone_ID, Stage, IP, Port, Return_To, Pre_Dispatch, Vaild_Input, Allow_Shift, Buf_Constrain, OpenDoorAssist, Type, Enabled |
|----|

　　檔案選取完畢後會將檔案內資料帶入預覽，可進行確認是否為匯入工作站。

![](media/image429.png)

### 4.3.2 匯出工作站（Export Floor Workstations）：

　　點擊後，可以將當前的工作站資料匯出成 Excel 檔案，方便備份或進一步處理。

### 4.3.3 手動新增（Add Row 、 Add Column）：

![](media/image68.png)

　　可依機台數量需求新增設備項目列或欄位進行填寫。

![](media/image13.png)

　　 例：今天要新增兩組機器，一組機器有六個製程，一個製程一台機器，所以共十二台。

　　此時我可以點擊 『新增欄位（Add Column）』 六次，添加六列，再點擊 『新增列（Add Row）』 一次，添加一行，這樣就會同下圖，總共十二台機器。

![](media/image285.png)

　　若想將多餘的欄位刪除，點擊位於行列上的 紅色叉叉，將整列或整行刪除。

　　新增刪除的規則是整列整行進行處理，那麼有單台項目的該怎麼辦呢？

　　若因為排序問題想進行調整，我們先接下來了解下面的 工作站表格欄位（Workstation Table Fields）。

![](media/image308.png)

### 4.3.4 工作站表格欄位 ( Work Station Form )：

![](media/image335.png)

#### 4.3.4.1刪除按鈕（Delete Button）：

　　依位置而異，若位於左側則刪除整行，若位於上方則刪除整列。點擊即刪除，請注意填寫的資訊是否已儲存，避免資料遺失。

#### 4.3.4.2 工作站 ID（Workstation ID）：

　　機台（Port）名稱，需與地圖編輯設定中該機台的名稱相同，後文會再次提醒。

#### 4.3.4.3 設備 ID（Equipment ID）：

　　機台名稱，例如該 Port（Workstation）ID 是 QWUET03-1，其中 QWUET03 是機台名稱，1 代表第一個 Port。

#### 4.3.4.4 區域 ID（Zone ID）：

　　該機台（Port）屬於哪個區域（自走車可選擇於哪個區域工作）。預設為「other」，為下拉式選單，資料來源為 區域管理（Zone Management） 頁面。

#### 4.3.4.5 Stage：

　　機台（Port）屬於哪一階段的製程群組。

#### 4.3.4.6 IP 位址（IP Address）：

　　機台的 IP 位址，請與相關人員確認對應的 IP。開啟模擬時，此項目不會出現。

#### 4.3.4.7 連接埠（Port）：

　　機台的連接埠，預設為 5000，請與相關人員確認對應的連接埠。開啟模擬時，此項目不會出現。

#### 4.3.4.8 Return to：

　　當物料生產完成後，放置在哪個貨架位置。

#### 4.3.4.9 預先派送（Predispatch）：

　　目前此功能應無作用。

#### 4.3.4.10 設備進出貨選項：

　　使用預設 (LotIn&LotOut) 即可，其餘都是特殊客戶開發。

![](media/image78.png)

#### 4.3.4.11 有效輸入（Valid Input）：

　　若客戶機台沒有 E84 訊號，TSC 可支援透過詢問上位系統的方式，確認機台能否進行上下料。此設定是針對整個專案（Project）的，開啟後所有工作站（Workstation）都會進行詢問。如果有特定機台不想進行詢問，可以取消勾選此選項，該機台就不會進行詢問。

#### 4.3.4.12 限制擺放位置（Buf Constrain）：

　　若該工作站（Workstation）位於通道很窄的地方，空間只夠手臂將載具 Carrier 放置在上層，可勾選此選項。

　　勾選後，該工作站的 Carrier 就只會放在上層。

#### 4.3.4.13 開門輔助（Open Door Assist）：

　　特殊機台需先開啟罩子，TSC 會先詢問上位系統。**此為特殊需求設定，使用前須先與相關人員確認。**

#### 4.3.4.14 允許位移（Allow Shift）：

　　若勾選此選項，系統會允許自走車在該工作站（Workstation）進行輕微的位置調整，以確保 Carrier 能夠精確放置或取貨。此功能適用於需要高精度對接的機台，但使用前請確認現場環境是否適合進行位移調整。

#### 4.3.4.15 啟用（Enable）：

　　是否要上線。

### 4.3.5 展開全部（Expand All）：

![](media/image45.png)

　　當新增的工作站（Workstation）數量過多時，頁面資料可能會顯得混雜。此時，可以透過 展開全部（Expand All） 按鈕，一次性打開或隱藏大部分資料。

　　若只想查看特定機台的資訊，也可以點選該機台旁邊的 藍色箭頭按鈕，單獨展開該機台的詳細內容。

### 4.3.6 切換樓層（下拉選單）：

![](media/image384.png)

　　當一個專案包含多個樓層時，可以透過下拉選單切換樓層地圖，並編輯該地圖上的工作站分配。

### 4.3.7 存檔（Save）：

![](media/image164.png)

　　無論是新增、修改或匯入資料，操作完成後請記得點擊存檔按鈕以保存變更。

## 4.4 區域管理 ( Zone Management )

![](media/image63.png)

　　進入區域管理頁面，我們能看到上圖的畫面，若畫面中出現下圖時：

| ![](media/image69.png) | 禁止編輯符號，如看見此符號，則代表未將 TSC 系統 暫停，請至 自走車看板（Vehicle Dashboard） 將 TSC 系統 暫停後，再進行修改。 |
|----|----|

![](media/image284.png)

**　　如果需要使用此處的編輯選項，請先至 自走車看板（Vehicle Dashboard） 的位置，將 TSC 系統 暫停。**

![](media/image74.png)

　　暫停後，方可進行設定變更，修改完畢請記得回到此處啟用 TSC 系統。

![](media/image221.png)

　　暫停後回到區域管理頁面，能發現編輯選項被解鎖了。

### 4.4.1 新增區域功能列 ( Add New Zone )：

　　在欄位中輸入區域名稱。

　　點擊「新增」按鈕。

　　區域命名的規則建議與相關人員討論。

### 4.4.2 區域列表：

![](media/image234.png)

#### 4.4.2.1 區域名稱 (Zone Name)：

　　例如 zone1。具體命名規則建議與相關人士討論。

#### 4.4.2.2 相鄰區域 (Neighbor Zone)：

　　依現場需求，若需要協助支援的區域，可加入相鄰區域。

#### 4.4.2.3 排程演算法（Schedule Algo）：

　　這個欄位用於選擇區域的演算法，選項包括：

![](media/image337.png)

　　by_lowest_cost：

　　　　收集的指令會按照整體最優路線執行。

　　　　同一個 port 有交換貨指令時，一定會先下後上。

　　by_better_cost：

　　　　指令會依照出發地和目的地進行分區處理。

　　　　出發地為電子貨架（erack）的指令會將整群電子貨架（erack）視為整體來單獨計算最短路線，並且將目的地的機台視為整體來單獨計算最短路線後執行。

　　by_fix_order：

　　　　按照地圖中點的 order 來當作執行指令的順序。

　　by_priority：

　　　　按照指令的優先級 ( Priority ) 來當作執行順序，不考慮距離效率。

　　　　預設演算法為 by_lowest_cost，這是效率最高且最推薦的選項。其餘演算法是針對特殊機台或需求開發的，如需使用請先與相關人員討論。

#### 4.4.2.4 車輛演算法（Vehicle Algo）：

#### ![](media/image279.png)

　　by_lowest_distance：

　　　　系統自動計算所有自走車與目標點的距離。

　　　　優先派遣目前位置最近的自走車執行任務。

　　by_battery：

　　　　篩選電量充足的自走車，一般由最高電量進行選擇。  
　　　　從符合條件的車輛中隨機選擇。

#### 4.4.2.5 最大合併命令數 (Merge Max Cmds)：

　　設定自走車執行批次搬移命令的數量，最多設定為『6』，即三組命令，同 TSC 設定中的『批次任務設定 ( Batch run ) 』。

　　此處可依各區域需求調整不同的任務數量。

#### 4.4.2.6 任務合併前置時間 (Merge Start Time)：

　　合併的初始時間，在批次任務合併時的前置等待時間，提供足夠的時間進行事前準備。

![](media/image342.png)

#### 4.4.2.7 任務合併集結時間 ( Collect Timeout )：

　　命令收集的超時時間。收集批次命令的區間結束時間，設定幾秒就會使用幾秒來等待任務輸入，當收集到一個任務後，此時間會重新計算，直到下一個任務輸入。

![](media/image286.png)

　　若時間到或任務集齊所需數量，則會結束任務集結，要求自走車執行此批次任務。

#### 4.4.2.8 最大合併設備數 (Merge Max Eqps)：

　　若自走車在該區域中服務過多的機台，可能會降低生產效率，在此可指定此區域的最大服務的設備數量，不讓自走車服務過多的機台，將多餘的任務發配給其他自走車執行。

#### 4.4.2.9 指令存活時間（Command Living Time）：

　　當指令在等待隊列（Transfer Waiting Queue）中超過設定的時間仍未執行時，系統會自動取消該筆指令。單位為秒。

#### 4.4.2.10 Action：

　　操作功能選項，如編輯或刪除。

## 4.5 搬運統計看板 ( Transfer Statistics )

![](media/image28.png)

### 4.5.1 功能選單 ( Options )：

#### 4.5.1.1 時間篩選 ( Date Time )：

![](media/image3.png)

　　可依需求進行統計資料的日期範圍選取。

#### 4.5.1.2 重新整理 ( Refresh )：

![](media/image65.png)

　　點擊後可重新獲取對應的最新資料。

#### 4.5.1.3 自走車切換選單 ( AMR Selection )：

![](media/image30.png)

　　可依需求進行切換查看各車數據。

### 4.5.2 自走車狀態 ( MR Status )：

![](media/image98.png)

![](media/image160.png)

　　可選擇特定時間的自走車狀態報告進行匯出。

　　這張圖表顯示了車輛在一天中各種運作狀態下所花費的時間百分比，讓使用者能快速了解車輛的主要活動內容，例如：

1.  執行任務的時間

2.  充電的時間

3.  停機或維護的時間

　　圖表軸線說明：

　　　　Y 軸 代表日期。

　　　　X 軸 代表時間百分比 (0% 到 100%)。每個區段代表車輛狀態。區段的長度表示該狀態佔當天總時間的百分比。

　　圖例狀態解說：

| 狀態代碼 | 中文名稱 | 說明 |
|----|----|----|
| Run | 執行搬運任務 | 車輛正在移動、取貨或放貨，執行實際搬運任務。 |
| Charge | 充電 | 車輛正在進行電池充電，通常在充電站或指定區域。 |
| Avail | 剩餘時間 | 當天結束時未被計入標準狀態的剩餘時間，通常為閒置或未定義狀態。 |
| Down | 停機 | 因嚴重警報或故障導致的停止運行，需等待處理。 |
| W_EN | 等待處理 | 因警報暫停運行，等待技術人員處理或解除警報。 |
| NM | 閒置 | 車輛未執行任何特定任務，處於完全閒置狀態。 |
| Test | 測試 | 因測試需求導致的臨時停止，通常為非正常運作狀態。 |
| PM | 手動控制/維護 | 車輛處於手動控制模式或計劃性維護，通常為計劃內的停機。 |

### 4.5.3 合併指令 ( Commands Merger )：

![](media/image53.png)

　　這張圖表用於監督系統每日指派給車輛的任務數量分佈，幫助使用者了解：

1.  系統是否傾向於一次指派多個任務

2.  車輛的工作負載模式是否均衡

3.  任務調度的策略是否有效

　　圖表軸線說明：

1.  Y 軸：代表當天所有指派事件的總和，顯示每種指派數量的發生次數。

2.  X 軸：代表不同的時間段，包括：當日、當週、當月。

　　圖例狀態解說：

　　　　每個顏色區段的高度代表特定合併數量的指派發生了多少次，例如：

1.  carrier(多少筆command))/per time(一個queue): 3

> 表示當天發生了3次任務指派事件，每次指派都只包含1個指令。

2.  carriers/per time: 201

> 表示當天發生了201次任務指派事件，每次指派都合併了4個指令。

### 4.5.4 搬運量 ( Transfers )：

![](media/image17.png)

![](media/image160.png)

　　可選擇特定時間的自走車狀態報告進行匯出。

　　這張圖表用於統計每日搬運任務 (Transfer) 的執行狀況與結果分類，幫助使用者掌握以下資訊：

1.  成功與失敗的搬運數量：了解整體搬運成功率。

2.  特定類型搬運數量：例如，到工作站裝/卸貨的搬運次數。

3.  嚴重問題數量：可能影響效率或安全的嚴重警報。

　　圖表軸線說明：

1.  Y 軸 (左側 - Total Completed)：代表搬運次數的總體完成情況（成功加失敗的總和），以及伴隨發生的嚴重警報數量。

2.  Y 軸 (右側 - Load Transfer)：顯示成功完成的搬運任務中，到工作站 (Workstation) 的次數，關注特定類型操作（裝/卸貨）的執行頻率。

3.  X 軸：代表不同的時間段，包括：當日、當週、當月。

　　圖例狀態解說：

| 狀態代碼 | 中文名稱 | 說明 |
|----|----|----|
| Successful | 成功搬運次數 | 當天成功完成的總搬運次數，顯示整體運作效率。 |
| Failed | 失敗搬運次數 | 當天失敗的總搬運次數，反映系統或車輛的問題。 |
| Load | 工作站搬運次數 | 當天成功完成且目的地是工作站 (Workstation) 的搬運次數，關注裝/卸貨頻率。 |
| Serious | 嚴重警報次數 | 當天記錄到的與搬運相關的嚴重警報次數，可能影響效率或安全。 |

### 4.5.4 平均搬運時間 ( Transfers Average Time )：

![](media/image101.png)

　　這張圖表用於顯示完成搬運任務所花費的平均時間，幫助使用者了解搬運效率，並找出可能影響效率的因素。

　　圖表軸線說明：

1.  Y 軸：代表「平均時間 (Average Time)」，單位為秒 (Seconds)，顯示每個時間段的搬運任務平均耗時。

2.  X 軸：代表不同的時間段，包括：當日、當週、當月。

### 4.5.5 錯誤代碼 ( Result Code )：

![](media/image293.png)

　　這張圖表用於檢查搬運任務 (Transfer) 的最終結果狀態碼，幫助使用者快速了解每次搬運任務的成功或失敗情況，並分析失敗原因。

　　圖表軸線說明：

1.  X 軸：代表「發生次數 (Counts)」，顯示每種狀態碼的出現頻率。

2.  Y 軸：代表「不同的 Result Code 原因」，顯示各種失敗原因的代碼。

### 4.5.5 當月完成搬運量 ( Transfers Completed This Month )：

![](media/image373.png)

　　這張圖表提供當月累計搬運完成次數的快速概覽，讓使用者能夠即時掌握從月初到目前為止的總搬運次數，幫助評估整體運作效率與目標達成情況。

### 4.5.6 今日警報數量 ( Alarm Frequency Today )：

![](media/image43.png)

　　這張圖表提供當天（從今天開始到目前為止）系統所記錄到的警報次數，並依照警報的狀態進行分類統計，幫助使用者快速掌握系統的健康狀況與潛在風險。

　　圖例狀態解說：

| 狀態代碼 | 中文名稱 | 說明 |
|----|----|----|
| Total | 總警報次數 | 當天所有警報的總數，包含警告、錯誤與嚴重警報。 |
| Warning | 警告警報次數 | 當天發生的警告警報數量，通常為輕微異常，需注意但無立即風險。 |
| Error | 錯誤警報次數 | 當天發生的錯誤警報數量，表示系統或設備出現問題，需進一步檢查。 |
| Serious | 嚴重警報次數 | 當天發生的嚴重警報數量，可能影響系統運作或安全，需立即處理。 |

### 4.5.7 距離上次警報時間 ( Time Since Last Alarm )：

### ![](media/image58.png)

　　這張圖表可顯示系統最近一次發出警報後，直到目前為止所經過的時間，協助使用者掌握系統最新的警告狀態。

## 4.6 自走車統計看板 ( Vehicle Statistics )

　　因頁面篇幅過長，在此分段說明。

### 4.6.1 功能選單 ( Options )：

![](media/image249.png)

#### 4.6.1.1 時間篩選 ( Date Time )：

![](media/image3.png)

　　可依需求進行統計資料的日期範圍選取。

#### 4.6.1.2 重新整理 ( Refresh )：

![](media/image65.png)

　　點擊後可重新獲取對應的最新資料。

#### 4.6.1.3 自走車切換選單 ( AMR Selection )：

![](media/image30.png)

　　可依需求進行切換查看各車數據。

### 4.6.2 30天內端口阻塞時間 ( Port Blocking Time In 30 Days )：

![](media/image159.png)

　　這張圖表提供過去 30 天內系統中各 Port（端口）的阻塞時間統計，協助使用者快速識別哪些端口的阻塞時間最長，以便進一步針對性地進行優化或排除故障。

　　圖表軸線說明：

1.  X 軸（端口名稱）：顯示系統中不同的 Port（端口）名稱。

2.  Y 軸（阻塞時間，單位：秒）：顯示每個 Port 的總阻塞時間，單位為秒。

3.  長條高度：每個長條的高度對應該 Port 的總阻塞時間數值，數值會直接標示在長條上方。

4.  排序：圖表中的 Port 會按照阻塞時間由長到短進行排序，讓使用者一目了然地看出哪些 Port 的阻塞時間最長。

### 4.6.3 車輛數據 ( Vehicle States )：

![](media/image376.png)

　　這張圖表提供車輛在不同時間段（24小時/7天/30天）內的活動分佈，讓使用者能夠透過觀察各狀態的佔比以及整體利用率，評估車輛的運行效率和工作飽和度。

　　了解利用率 (Utilization Rate)：利用率（Utilization Rate）是指車輛處於生產性活動狀態的時間總和，佔所選時間範圍內總時間的百分比。

![](media/image379.png)

　　圖例狀態解說：

<table>
<colgroup>
<col style="width: 13%" />
<col style="width: 14%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;">狀態代碼</th>
<th style="text-align: center;">中文名稱</th>
<th style="text-align: center;">說明</th>
</tr>
<tr>
<th>Acquire</th>
<th>取貨</th>
<th>車輛正在執行從指定地點（如貨架、工作站）拾取貨物的動作。此狀態通常涉及精確定位、升降、夾取或其他機械操作。</th>
</tr>
<tr>
<th>Moving</th>
<th>移動</th>
<th>車輛正在路徑上行駛，從一個點移動到另一個點。這可以是在取貨後載著貨物移動，也可以是空車前往下一個任務點（如貨架或充電站）。</th>
</tr>
<tr>
<th>Deposit</th>
<th>放貨</th>
<th>車輛正在執行將攜帶的貨物放置到指定地點（如貨架、工作站）的動作。此狀態與「取貨」相對，通常涉及放置貨物的操作。</th>
</tr>
<tr>
<th>Pause</th>
<th>暫停</th>
<th>車輛暫時停止了當前的活動。這可能是由於指令或操作員介入等原因，但並非完全閒置或故障。</th>
</tr>
<tr>
<th>Charge</th>
<th>充電</th>
<th>車輛位於充電站並正在進行電池充電。此狀態表示車輛正在為下一次任務充電。</th>
</tr>
<tr>
<th>Standby</th>
<th>等候</th>
<th><p>車輛處於準備接收任務的狀態，但當前沒有任務執行。</p>
<p>包括：</p>
<ol type="1">
<li><p>充電完成後，仍然停留在充電站等待。</p></li>
<li><p>停在系統指定的待命點或停車區等待任務分配。</p></li>
<li><p>在完成一個任務後，等待下一個任務指令的短暫間隙。</p></li>
</ol></th>
</tr>
<tr>
<th>Idle</th>
<th>閒置</th>
<th>車輛沒有被分配任何任務，也沒有處於充電或特定待命狀態，基本上是完全待機。此狀態表示車輛目前未被使用，可能需要檢查是否有待分配的任務或系統配置問題。</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

　　透過此功能，使用者可以清晰了解車輛在不同時間段的活動狀態與利用率，從而評估車輛的運行效率及工作飽和度，便於進行後續的優化或調整。

### 4.6.4 車輛運行狀態紀錄 ( Vehicle States Logs )：

![](media/image153.png)

　　這張表提供一個詳細的歷史記錄查看器，展示每一輛自走車狀態變化的流水帳。使用者可以通過查詢和篩選特定時間範圍或關鍵字的狀態變更事件，查看包含時間、任務ID、車輛ID、狀態、目的地、電池電量等詳細資訊的原始記錄。此功能主要用於深入追蹤、問題排查和數據導出分析。

### 4.6.5 車輛警報紀錄 ( Vehicle Alarm Logs )：

![](media/image185.png)

　　這張表專門用於展示與自走車相關的歷史警告事件。使用者可以通過查詢特定時間範圍或關鍵字，查看包含警告時間、車輛ID、級別、代碼、原因、詳細描述等信息的記錄。主要用途包括追蹤車輛故障、診斷問題以及進行警告分析。

### 4.6.6 電池資訊紀錄 ( Battery Info Logs )：

![](media/image264.png)

　　這張表提供自走車的電池狀態歷史數據，允許使用者透過車輛 ID 和時間範圍進行篩選查詢。表格會顯示特定時間點的電池容量、電壓、電流、健康度、溫度、是否在充電以及電池ID等關鍵指標。主要用途包括監控電池健康狀況、分析歷史性能數據，並輔助電池維護。

### 4.6.7 啟動電池數據統計( Starting Battery Statistics )：

![](media/image202.png)

　　此項目需要透過點擊才會主動獲取對應的電池數據並且列出，點擊後將會出現兩個圖表。

#### 4.6.7.1 電量指示條 ( Battery bar )：

![](media/image57.png)

　　這張圖表監控車輛在過去 30 天內「電池容量 (Battery Capacity)」和「電池健康度 (Health)」隨時間變化的歷史趨勢。

　　圖表軸線說明：

1.  X 軸: 顯示過去 30 天的歷史紀錄範圍。

2.  Y 軸 (左側 - Battery Capacity): 顯示電池容量的百分比。

3.  Y 軸 (右側 - Battery Health): 顯示電池健康度的百分比。

　　圖例狀態解說：

| 狀態代碼 | 中文名稱 | 說明 |
|----|----|----|
| Battery Capacity | 電池容量 | 電池當前充滿電後能儲存的最大電量。反映電池的存儲能力，容量越高表示電池可以儲存更多的電量。 |
| Health | 電池健康度 | 電池健康度的百分比。評估電池整體狀況的指標，通常綜合了容量衰減、內阻增加等多方面因素。健康度越高表示電池狀況越佳。 |

#### 4.6.7.2 自走車月平均充電時間 ( Average Charge Time in 30 Days Per Vehicle )：

![](media/image127.png)

　　這張圖表顯示車輛在過去 30 天內的充電時間統計數據，幫助使用者了解車輛的平均充電耗時和近期總充電負擔。

##### 4.6.7.2.1 過去 30 天內平均充電時間 (Average Charge Time in 30 Days Per Vehicle)：

　　平均充電耗時 (charge average time)：在過去 30 天內，每一次完整充電過程的平均持續時間。

　　總充電時間 (total charge time)：在過去 30 天內，該車輛所有充電過程的總時長累加。

##### 4.6.7.2.2 每月充電完成次數統計 (Count for Aqurice to Charge Per Vehicle)：

　　圖表軸線說明：

1.  X 軸：代表不同的月份。

2.  Y 軸 (Total Completed)：代表在對應月份內，該車輛完成充電的總次數。

##### 4.6.7.2.3 充電循環次數 (Number of Charging Cycles Per Vehicle)

　　顯示車輛電池累計經歷了多少次完整的充電循環。一個充電循環通常指電池從滿電狀態放電再充滿的過程，或者等效的累計充放電量。

### 4.6.8 電池資訊 ( Vehicle battery information )：

![](media/image334.png)

　　這個圖表允許使用者選擇特定的車輛和時間範圍，深入觀察該車輛電池的各項關鍵性能指標（包括整體指標和單個電芯指標）在該時間段內的變化趨勢。透過詳細、可互動、基於時間序列的監控版，使用者可以即時掌握電池的健康狀況與運作效率。

#### 4.6.8.1 電池資訊統計 ( Battery Info Staticstics )：

![](media/image410.png)

　　使用者可以直觀地看到電池的電壓、電流、溫度和健康度是如何隨著時間推移而變化的。展示選定車輛的「整體電池包」關鍵性能指標在指定時間範圍內的變化趨勢。

　　圖例狀態解說：

| 狀態代碼 | 中文名稱 | 說明 |
|----|----|----|
| Voltage | 電壓 | 電池的電壓值，反映電池的充放電狀態。通過觀察電壓的變化，可以了解電池的充放電進程及是否存在異常波動。 |
| Current | 電流 | 電池當時的工作負載或充電速率。用於分析車輛的能耗情況或充電效率。 |
| Temperature | 溫度 | 電池的實時溫度值。通過溫度監控，可以及時發現電池過熱或過冷的情況，進而採取相應措施。 |
| Health | 健康度 | 隨著使用和時間推移，電池容量會衰減、內阻會增加，導致健康度下降。用於長期監控電池性能，判斷是否需要更換電池或進行維護。 |

#### 4.6.8.2 電池單元統計 ( Battery Cells Staticstics )：

![](media/image298.png)

　　展示電池內每個獨立電芯的電壓變化曲線，讓使用者能夠深入了解電池內部的健康狀況和均衡性。這是診斷電芯不均衡、識別弱電芯、評估功能以及保障電池整體壽命和安全性的關鍵圖表。

## 4.7 命令歷史紀錄 ( Transfer Commands )

### 4.7.1 命令紀錄頁籤 ( Commands Tab )：

![](media/image275.png)

#### 4.7.1.1 功能選單 ( Options )：

##### 4.7.1.1.1 匯出資料表 ( Export )：

![](media/image320.png)　　　　![](media/image124.png)

　　點擊此按鈕後，會出現彈跳視窗，請依照需要的時間範圍內選取並進行匯出。

##### 4.7.1.1.2 重新整理 ( Refresh )：

![](media/image197.png)

　　點擊此按後，將會清空篩選條件並重新獲取資料，操作時請注意自己欲查詢的項目。

##### 4.7.1.1.3 搜尋 ( Search )：

![](media/image330.png)

　　此資料表的搜尋條件為時間範圍與 Carrier ID，時間範圍選取後自動進行資料搜尋，Carrier ID 則需要在輸入完後按下 Enter 才會進行搜尋。

##### 4.7.1.1.4 資料表 ( Data Table )：

![](media/image119.png)

　　這張圖表幫助使用者快速找到特定命令記錄並處理執行失敗的命令，確保系統運作順暢，點擊左側的綠色＋號可展開詳細資訊。

　　使用者可以透過以下條件快速找到特定的命令記錄：

1.  時間範圍：選擇特定日期或時間段。

2.  車輛 ID：輸入特定車輛的編號。

3.  命令類型：過濾特定類型的命令（如搬運、充電、維護等）。

4.  執行狀態：過濾成功或失敗的命令記錄。

　　應用場景：

1.  故障排查：快速找到某輛車在某時間段的失敗命令，分析原因。

2.  歷史追蹤：查看特定車輛的命令執行記錄，了解運作情況。

3.  數據分析：過濾特定類型的命令，進行統計分析。

4.  進行重試：查詢到失敗的命令後，至操作介面重新下達命令。

### 4.7.2 退回命令紀錄頁籤 ( Rejected Commands Tab )：

![](media/image132.png)

　　這張圖表用於記錄系統接收到搬運命令後，因檢查發現問題而被「拒絕執行」的命令。幫助使用者快速找出哪些命令因為格式或參數錯誤而無法被系統接受，以便修正命令的生成邏輯或檢查相關設定。

## 4.8 搬運任務看板（Transfer Dashboard）

![](media/image397.png)

此看板有五個重要區塊，依序號順序為：

1.  等待佇列（Transfer Waiting Queue）

2.  執行佇列（Transfer Execution Queue）

3.  手動添加單筆任務（Manual Input）

4.  批次執行多筆任務（Batch Run）

5.  循環測試任務（Test Run）

### 4.8.1 等待佇列（Transfer Waiting Queue）

![](media/image4.png)

　　此列表會顯示等待執行中的搬移任務（Transfer Tasks）。

　　當新任務添加至 TSC 系統 後，會先送至 等待佇列（Waiting Queue） 中等待。

　　排程會合併任務，指派給適合接取任務的自走車執行。

　　除了顯示操作者從 Secs Protocol 輸入到 TSC 系統 中的搬移指令執行狀態外，也可透過介面手動添加任務。

### 4.8.2 執行佇列 (Transfer Executing Queue)

![](media/image11.png)

　　自走車接取並執行的任務會列在此處。

　　排程規則（Scheduling Rules）：

> 　　當有多筆任務時，會有集貨機制，將目的地附近的載具一起運送，減少來回時間。系統會計算最短路徑，以最快方式送達。

　　不會事先確認機台狀態，接收到指令時便運送。

### 4.8.3 手動添加單筆任務 ( Manual Input )

![](media/image295.png) 　　　　　　![](media/image223.png)

#### 4.8.3.1 載具 ID（Carrier ID）：

　　載具的 ID，如不指定，請留空。

#### 4.8.3.2 載具類型（Carrier Type）：

　　該指令指定載具的類型，確保自走車能夠正確識別與處理。

#### 4.8.3.3 優先度（Priority）：

　　執行優先度（建議 1-99 之間），數字越高優先度越高。

#### 4.8.3.4 來源位置（Source）：

　　載具的來源位置。

|  | 有 Carrier ID | 無 Carrier ID |
|----|----|----|
| 有選擇來源位置 | 確認無誤後正常送入等待佇列。 | 尋找來源位置Carrier ID，若有貨物會進入等待佇列。 |
| 無選擇來源位置 | 尋找該Carrier ID 所在位置，送入等待佇列。 | 跳出錯誤警示，來源不名，貨物不明。 |

#### 4.8.3.5 目的地（Destination）：

　　載具的目的地。

|  | 有勾選交換 | 無勾選交換 |
|----|----|----|
| 有選擇目的地 | 確認目的地有無貨物可供交換，有的話正常送入等待佇列。 | 確認目的地有無貨物佔位，沒有的話正常送入等待佇列。 |
| 無選擇目的地 | 將貨物放置在AMR Buffer上。 | 將貨物放置在AMR Buffer上。 |

#### 4.8.3.6 交換（Replace）：

　　是否交換機台上的載具。

　　若勾選 交換（Replace），則會出現 Back，指的是交換貨的 載具（Carrier） 要去哪裡，而不是任務結束後返回的點。

#### 4.8.3.7 返回站點（Back）：

　　任務完成後所返回的站點。

#### 4.8.3.8 返回載具 ID（Back Carrier ID）：

　　返回的載具 ID。

#### 4.8.3.9 返回載具類型（Back Carrier Type）：

　　返回的載具類型。

4.8.3.10 執行延遲時間（Execute Delay Time）：

　　若指令需要到機台前執行 trload 或 trunload req 請求的話，等待時間則會以這個時間為主。

#### 4.8.3.11 新增 ( Add ) ：

　　完成後點擊 新增（Add），會將新任務增加至 等待佇列（Waiting Queue），待自走車接收任務。

![](media/image13.png)

　　將所在位置為 E2P1 且 載具 ID（Carrier ID） 為 GY001 的載具送至指定空儲位 E2P5。

　　此時有三種方法可下指令。

| 方法一 | 方法二 | 方法三 |
|----|----|----|
| ![](media/image421.png) | ![](media/image253.png) | ![](media/image360.png) |
| 系統會自動抓取 GY001 的所在位置，再送至目的地 E2P5，接著回到預設的返回點。 | 系統會確定 E2P1 是否有 GY001 這個 Carrier ID，有的話會送到目的地 E2P5，接著再回到預設的返回點。 | 系統會確認所有填入資訊是否正確，正確就照設定上的位置送完貨物後，再回到設定的返回點 C001。 |

![](media/image308.png)

### 4.8.4 批次執行多筆任務 ( Batch Run )

![](media/image268.png)

　　我們若要一次匯入大量指令時，可透過 批次執行多筆任務（Batch Run） 執行。首先點擊 選擇檔案（Select File），會出現上傳介面。

![](media/image349.png)

　　由於我們是第一次執行，可以先點擊 產生範本（Generate），將基本規格的檔案下載下來。範本檔是 CSV 檔，請確認當下是否能夠進行修改，若否請事前準備。

![](media/image8.png)

　　當範本檔下載下來後點開進行編輯，這裡我們可以填入範例資料中的項目，或是直接使用準備好的範例檔。建議還是實際編輯過會比較有印象。

![](media/image97.png)

　　上方是範例檔的規格，填寫完畢後存檔，回到上傳畫面。

![](media/image10.png)

　　點擊 選擇檔案（Choose a File）。

　　檔案選擇後會自動帶入資料內容呈現在畫面中，可以二次確認資料是否有錯誤。

![](media/image167.png)

　　資料確認無誤後點擊 匯入（Import），命令就會進入 等待佇列（Transfer Waiting Queue），發配給自走車去執行。

　　若命令錯誤會直接在 警示看板（Alarm Dashboard） 顯示。

####  

### 4.8.5 循環測試任務 ( Test Run )

　　將多筆任務分階段編輯在 JSON 檔 後，手動選擇檔案匯入，做循環測試。

#### ![](media/image44.png)

　　循環測試任務（Test Run） 與 批次執行多筆任務（Batch Run） 雷同，但 循環測試任務（Test Run） 可以重複發布命令，讓系統持續運作，進行多種壓力測試，藉此發現生產製程中的錯誤與極限。

![](media/image29.png)

　　同樣因為我們是第一次使用，可以先點擊 產生範例檔（Generate）。  
　　此處因為循環進行命令格式的原因，檔案的格式為 JSON 檔。

![](media/image402.png)

<span class="mark">　　JSON 的格式如下：</span>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th>[<br />
[<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "S1P1","Dest": "E2P10","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "E2P1","Dest": "S1P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "S1P1","Dest": "E2P3","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "E2P10","Dest": "S1P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" }<br />
],<br />
[<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "S1P1","Dest": "E2P3","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "E2P10","Dest": "S1P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" }<br />
],<br />
[<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "S1P1","Dest": "E2P12","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "E2P3","Dest": "S1P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" }<br />
],<br />
[<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "S1P1","Dest": "E2P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" },<br />
{"CommandID": "0","CarrierID": "GY001","CarrierType": "","Source": "E2P12","Dest": "S1P1","Priority": 0,"Replace": 0,"Back": "WSD001","BackCarrierID": "GY001","BackCarrierType": "","EXECUTETIME": "" }<br />
]<br />
]</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<span class="mark">其中單筆命令的格式為：</span>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th>{<br />
"CommandID": "0",<br />
"CarrierID": "GY001",<br />
"CarrierType": "",<br />
"Source": "S1P1",<br />
"Dest": "E2P10",<br />
"Priority": 0,<br />
"Replace": 0,<br />
"Back": "WSD001",<br />
"BackCarrierID": "GY001",<br />
"BackCarrierType": "",<br />
"EXECUTETIME": ""<br />
}</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<span class="mark">　　我們可以發現它就是欄位的格式化，因此在編輯循環測試命令時，部分命令可以先透過單筆命令執行，確定是否有問題，若無問題再加入。</span>

![](media/image381.png)

<span class="mark">　　當自己的測試檔編輯完畢，可以點擊 選擇檔案（Choose a File），選擇自己編輯好的測試檔，或是選擇範例文件的附帶測試文件。</span>

![](media/image284.png)

　　範例文件中的資料主要是針對模擬器（Simulator）使用，如有數據上的誤差，請更改成正確的版本，或針對現場的正確資訊進行填寫，避免出現問題。![](media/image221.png)

<span class="mark">　　</span>

<span class="mark">　　選定後，直接將 切換鈕（Toggle Switch） 打開，系統就會一直重複發送測試檔中的命令，直到你關閉。</span>

![](media/image241.png)

![](media/image72.png)

　　這時若命令中有錯誤，會持續出現在 錯誤警示（Error Alerts） 中，上方為正常發送。

## 4.9 地圖管理（Map Management）

![](media/image214.png)

　　左側的是地圖檔案列表，右側是讓我們連接自走車去取得地圖使用的。

![](media/image409.png)

　　 **地圖來源：**

　　地圖主要透過自走車（即我們所稱的 MR）在現場進行掃描獲取。您可能會發現，這些地圖與現有的地圖存在一些差異。這是因為現有的地圖已經經過處理，將掃描地圖中粗糙的部分進行優化，使其更加清晰且易於辨識。

![](media/image261.png)

### 4.9.1 上傳地圖 ( Upload Map )

　　新增地圖需透過上傳方式進行。請點擊按鈕並選取 PNG 格式地圖檔案，上傳完成後，相關檔案資訊將呈現於下方列表。如需圖檔，請聯繫相關人員取得。

![](media/image232.png)

### 4.9.2 上傳地圖列表 ( Upload Map )

| 檔案名稱 ( File Name ) | <span class="mark">顯示檔案的原始名稱。如需重新命名，請於上傳前完成更改。</span> |
|----|----|
| <span class="mark">檔案類型 ( Type )</span> | <span class="mark">請使用 PNG 格式圖檔。</span> |
| <span class="mark">上傳時間 ( Date Modified )</span> | <span class="mark">記錄檔案的上傳時間。</span> |
| <span class="mark">圖片尺寸 ( Dimensions )</span> | 記錄上傳圖片的尺寸與解析度。 |
| <span class="mark">檔案容量 ( Size )</span> | 記錄圖檔的容量大小。 |
| <span class="mark">操作 ( Action )</span> | 每個檔案均附帶刪除按鈕，點擊後將刪除該檔案。 |

### 4.9.3 自走車連接上傳 ( AMR Connect Upload )

![](media/image273.png)

　　透過與自走車的連接，系統可獲取地圖檔案。若需使用多張地圖，請記住所需地圖的名稱；若忘記名稱，亦可隨時返回確認。

| 檔案名稱 ( File Name ) | 顯示檔案的原始名稱。如需更改名稱，需由相關人員將圖檔從自走車取出，修改後再透過「上傳地圖」功能重新新增。 |
|----|----|
| 檔案類型 ( Type ) | 請使用 PNG 格式圖檔。 |
| 上傳時間 ( Date Modified ) | 記錄檔案的上傳時間。 |
| 圖片尺寸 ( Dimensions ) | 記錄上傳圖片的尺寸與解析度。 |
| 檔案容量 ( Size ) | 記錄圖檔的容量大小。 |
| 操作 ( Action ) | 每個檔案均附帶「轉移 (Transfer)」按鈕，點擊後將該圖檔匯入至本機的「本地上傳檔案列表」中。 |

## 4.10 地圖編輯（ Map Editor ）

![](media/image390.png)

### 4.10.1 地圖功能列 ( Map Options )

#### 4.10.1.1 地圖 ( MAP )

　　提供各種地圖編輯和操作選項，點開功能列上的地圖按鈕，出現如下圖。

![](media/image27.png)

##### 4.10.1.1.1 新增樓層 ( New Floor )

　　點選『新增樓層 ( New Floor )』，出現資料填寫視窗。

![](media/image311.png)

　　選擇地圖後接下來的選項才會出現。

![](media/image256.png)

###### 4.10.1.1.1.1 樓層名稱 ( Level Name )：

　　填寫該樓層的名稱，命名規則請詢問相關人員。

###### 4.10.1.1.1.2 地圖檔案 ( Map File )：

　　『地圖管理』中上傳的專案地圖會在此形成列表供選擇。

![](media/image409.png)

　　 每層樓都需要有它自己的地圖檔案。請不要把多個樓層都用同一張地圖，否則系統可能會出錯。

![](media/image261.png)

###### 4.10.1.1.1.3 層級 ( Z-index )：

　　圖層，可視為區域的流水編號，第一個新增的區域為『0』。

　　※ Z-index 編號為系統產生，依區域順序給予編號，如非必要請勿更改。

![](media/image284.png)

　　注意： 系統會自動為每個樓層生成一個叫做 "Z-index" 的編號，這個編號是按照區域順序排列的。除非有特殊需求，否則請不要修改這個編號。

　　舉例說明：

　　下面有三個專案的範例，每個專案都有多個樓層。系統會按照新增的順序為每個樓層分配編號。第一個樓層的編號預設為 0。具體的樓層順序應該根據實際使用需求來規劃，並建議與相關人員討論。

![](media/image318.png)

![](media/image221.png)

###### 4.10.1.1.1.4 自走車 IP ( Vehicle IP )：

　　因為第五項的路線檔為必填項目，為了讓系統知道自走車的行走路線，我們需要提供一個叫做「路線檔」的文件。這個文件可以通過兩種方式獲得：

　　連接自走車： 直接連接自走車，系統會自動從自走車上獲取該樓層的站點路線檔。

　　本地上傳： 如果你已經有路線檔存放在電腦上，可以直接上傳到系統中。

　　自走車路線檔：

　　當你輸入自走車的 IP 地址後，系統會自動連接自走車，並搜尋自走車對應資料夾中的路線檔。然後，系統會顯示一個下拉選單，讓你選擇需要的路線檔。

![](media/image424.png)

![](media/image354.png)

（ 使用此方式請確定自己欲選擇的路線檔為何 ）

![](media/image326.png)

（ 若 IP 填寫錯誤則會於右下角出現警示 ）

![](media/image409.png)

　　通常情況下，站點的位置需要與自走車的設定保持一致，否則自走車就無法正常運行。因此，我們建議盡量從自走車上匯入站點位置，而不是手動添加。

![](media/image261.png)

###### 4.10.1.1.1.5 路線檔 ( Local Route File )：

　　操作步驟：

　　　　點擊『自走車 IP ( Vehicle IP )』旁邊的『本地 ( Local )』按鈕。

　　　　出現『Local Route File』選項後，點擊『選擇檔案』按鈕。

　　　　選取您下載的範例路線檔。

![](media/image280.png)

###### 4.10.1.1.1.6 移動附加設定 ( Move Append )：

　　一般來說， 顯示 "No Available moveappend" 是正常的。

　　欄位填寫完成後，點擊『創建 ( Create ) 』，新增此樓層。

![](media/image314.png)

　　新增成功！ 畫面會顯示如上圖所示，您可以在上方功能列看到剛剛新增的樓層名稱。

![](media/image42.png)

　　如果未來有多個樓層，您可以通過下拉選單進行切換。

![](media/image409.png)

　　 建立站點資訊有兩種方式：

　　　　自己新增： 手動添加站點。

　　　　匯入： 從自走車獲取站點資訊並匯入到系統中。

　　通常，我們會先通過匯入自走車獲得的站點資訊，然後再通過系統介面進行細部設定。

　　只有在需要額外增加少量機台時，才會手動新增站點。 很少有情況是完全手動繪製所有站點的。

![](media/image261.png)

##### 4.10.1.1.2 存檔 ( Save ) 

　　可將編輯完成的地圖設定進行儲存。

![](media/image432.png)

![](media/image284.png)

　　※ 重要：建議每完成一個階段就進行存檔 ![](media/image221.png)

##### 4.10.1.1.3 刪除樓層 ( Delete Floor )

![](media/image14.png)

　　點擊確定後將會刪除該樓層，請謹慎使用此功能。

##### 4.10.1.1.4 地圖屬性設定 ( Map Display Settings)

　　設定地圖中各站點顯示狀況，包含顏色，大小，空心或實心點等等。

![](media/image184.png)

###### 4.10.1.1.4.1 臨界值 ( Threshold )

　　在地圖編輯過程中，針對兩點畫線時，系統會以圓心向外進行判定，其範圍單位為像素。為確保功能正常運作，如需修改此設定，建議先諮詢相關人員。

| ![](media/image391.png) | ![](media/image196.png) |
|----|----|
| Threshold：4 | Threshold：15 |

###### 4.10.1.1.4.2 方向標示顏色 ( Triangle Direction Colour )

　　可設定通行方向的標示顏色。

| ![](media/image179.png) | ![](media/image189.png) |
|----|----|
| RGB ( 108, 92, 231 ) | RGB ( 90, 230, 90 ) |

###### 4.10.1.1.4.3 站點填充顏色 ( Fill Colour )

　　可設定站點的填充顏色。

| ![](media/image178.png) | ![](media/image363.png) |
|----|----|
| RGB ( 0, 0, 255 ) | RGB ( 255, 180, 0 ) |

###### 4.10.1.1.4.4 站點外框顏色 ( Stroke Colour )

　　可設定站點的外框顏色。

| ![](media/image178.png) | ![](media/image218.png) |
|----|----|
| RGB ( 0, 0, 255 ) | RGB ( 255, 180, 0 ) |

###### 4.10.1.1.4.5 站點線條粗細 ( Stroke Width )

　　可設定站點的線條粗細。

| ![](media/image230.png) | ![](media/image358.png) |
|----|----|
| Stroke Width：3 | Stroke Width：10 |

###### 4.10.1.1.4.6 路徑線條 ( Path Stroke )

　　可調整在自走車看板（ Vehicle Dashboard）的路徑粗細。

| ![](media/image177.png) | ![](media/image7.png) |
|----|----|
| Size：3 | Size：15 |

###### 4.10.1.1.4.7 方向標示大小 ( Triangle Size \[WxH\] )

　　可調整方向標示的尺寸，但只能長寬等比例調整。

| ![](media/image412.png) | ![](media/image2.png) |
|----|----|
| Size：3 | Size：15 |

###### 4.10.1.1.4.8 地圖站點半徑 ( Radius )

　　單位為像素，可依下列對象設定該站點半徑，用於分辨站點使用。

| 充電站 (Charging Station) | 工作站 (Report Location) |
|----|----|
| ![](media/image201.png) | ![](media/image174.png) |
| Size：8 | Size：4 |
| 暫停點 (Stop Location) | 路口點 (Junction) |
| ![](media/image301.png) | ![](media/image115.png) |
| Size：5 | Size：4 |
| 交會點 (Connection Point) | 電池交換站 (Auto Battery Change Station) |
| ![](media/image188.png) | ![](media/image425.png) |
| Size：5 | Size：8 |

###### 4.10.1.1.4.9 站點實心狀態 ( Fill States )

　　可依下列對象進行設定，勾選該站點是否顯示為實心圓，以便於分辨站點的使用狀態。

![](media/image378.png)

　　經勾選的站點項目將固定顯示為實心圓。

##### 4.10.1.1.5 更新地圖站點 ( Fix Map Points )

　　點擊此功能後，會出現一個彈跳視窗，左上角有兩個項目頁籤。

![](media/image107.png)

###### 4.10.1.1.5.1 目前地圖站點 ( Current )

　　在此頁籤中，可以看到兩張列表，分別顯示站點位置與路徑的所有資料，並可在此處統一進行調整。

![](media/image242.png)

###### 4.10.1.1.5.2 比對地圖站點 ( Different )

　　進入此頁籤後，首先需要選擇資料來源進行比對。您可以輸入自走車 IP 進行連接以取得資料，或是匯入本地檔案。

![](media/image393.png)

　　輸入自走車 IP 並連接後，系統將顯示點位檔案列表。

![](media/image41.png)

　　載入後，右側會出現檔案選項。您可透過下拉選單選取欲載入的點位檔案，並點擊「LOAD」進行載入。

![](media/image104.png)

　　載入完成後，下方將顯示點位內容。

![](media/image260.png)

　　比對表單的規則是：若點位與現有資料相同，則不會顯示；若點位不存在於現有資料中，則會列於右方。若有需要新增的站點，可點選「ADD」按鈕進行加入。

##### 4.10.1.1.6 更換地圖 ( Change Maps )

　　點擊此功能後，會出現彈跳視窗，可以發現它有下拉選單跟新舊地圖的表格。

![](media/image296.png)

　　這時候點擊下拉選單，可以發現可供替換的地圖，然後進行選取。

![](media/image271.png)

![](media/image409.png)

　　 有人可能會發現，為什麼在地圖管理有那麼多地圖，為什麼只有一個檔案可以選擇？這是因為地圖解析度。

　　地圖解析度攸關到頁面的顯示比例，所以只有解析度是相同的情況下才可進行替換。假設解析度不同仍可替換的話，實際上看板的地圖跟點位都會錯位。

![](media/image261.png)

![](media/image237.png)

　　選取後對應的參數也會顯示在上面，之後按下存檔 ( Save )，就會進行替換了，不過這只是針對地圖的部分。

![](media/image136.png)

　　如同之前所說，在這裡進行存檔 ( Save )，才能存入整體專案，否則換頁之後這些變更都會消失。

##### 4.10.1.1.7 產生站點標籤 ( Generate Station Label )

![](media/image251.png)![](media/image227.png)![](media/image411.png)

　　點擊後，系統會將所有包含 Station ID 的站點，以 Station ID 作為標籤顯示於地圖上。站點標籤可幫助您辨識站點名稱，或標示重要站點。您可將這些標籤拖曳至合適的位置，以便在任務進行時快速定位問題發生的位置。

##### 4.10.1.1.8 下載 PNG 圖檔 ( Download PNG )

![](media/image352.png)　![](media/image267.png)

　　下載當前的圖檔。點擊後，系統將提示您輸入圖檔名稱，輸入完畢後，系統會直接下載當前已完成站點與路徑繪製的地圖，以供留存。

#### 4.10.1.2 繪製功能 ( Draw )

##### 4.10.1.2.1 路徑 (Path)

　　新增至少兩個「站點 (Point)」後，可點擊「路徑」功能按鈕開啟繪製功能進行連線。

　　繪製方式為：點擊第一個目標站點的圓心，按住滑鼠拖曳至第二個目標站點的圓心，系統將自動連接路徑。此操作較易出錯，可參考下方「繪製兩點一線」的範例以更清楚理解。

　　繪製完成後，請點擊功能列右側的 鎖定移動（Lock Move）按鈕，以避免既有資訊被改動。

![](media/image284.png)

　　若繪製路徑時未拖曳至圓心範圍內，系統將顯示錯誤提示。圓心的判斷範圍取決於「基本設定」中的臨界值。![](media/image221.png)

##### 4.10.1.2.2 站點 ( Point )

　　站點構造說明：

![](media/image255.png)

　　「Threshold」為繪製路徑時的反應範圍，常見錯誤為未點擊到範圍內。

![](media/image13.png)

　　**範例：繪製兩點一線**　

1.  點擊「站點」功能按鈕。

![](media/image356.png)

2.  在地圖上點擊兩個位置，下方示意圖顯示兩個站點的位置。

![](media/image80.png)

3.  點擊「路徑」功能按鈕。

![](media/image252.png)

4.  按住滑鼠從 A 站點中心拖曳至 B 站點中心，放開滑鼠後，線條將自動生成。

![](media/image131.png) ![](media/image92.png) ![](media/image414.png)

5.  繪製完成後，請點擊功能列右側的鎖定移動（Lock Move）按鈕，以避免既有資訊被改動。

![](media/image36.png)

6.  若路徑連線錯誤，系統將於左下角顯示提示。

![](media/image353.png)

![](media/image308.png)

##### 4.10.1.2.3 工作站 ( Workstation )

　　點擊該按鈕後，直接在地圖想要新增的位置進行點擊，會出現工作站的圖示。

![](media/image225.png)

　　例如希望在地圖顯示 電池交換站 ( ABCS ) 等設備時，可以建立一個，與該設備連線成功後會顯示對應的詳細資訊。

##### 4.10.1.2.4 錨點 ( Anchor )

　　點擊該按鈕後，直接在地圖想要做為瀏覽中心點的位置進行點擊，會出現錨點的圖示。

　　儲存後，前往自走車看板 (Vehicle Dashboard) 時可發現該錨點在地圖上的位置，直接點擊該錨點，地圖會以該錨點為中心直接移動並放大，便於觀察該區域的狀態。

##### 4.10.1.2.5 鎖定移動（Lock Move）

![](media/image36.png)

　　當 鎖定移動（Lock Move） 亮起時，請注意此時無法使用其他與 繪製 ( Draw ) 有關的功能。若需要進行其他新增物件的操作，請點擊你想要使用的按鈕來切換功能。　

　　而當 鎖定移動（Lock Move） 亮起時，此時可進行站點的移動。

##### 4.10.1.2.5 站點移動（Point Move）

　　此處有兩項移動功能，必須要點擊站點時，該功能才會顯示，如下圖：

![](media/image39.png)

###### 4.10.1.2.5.1 X軸座標修改器 ( X-Avis )：

![](media/image175.png)

　　選取站點點後再使用此功能進行移動，可在站點過於密集時使用，點擊箭頭將之移出，路徑連接完成後再移回去。

###### 4.10.1.2.5.2 Y軸座標修改器 ( Y-Avis )：

![](media/image426.png)

　　選取站點點後再使用此功能進行移動，可在站點過於密集時使用，點擊箭頭將之移出，路徑連接完成後再移回去。

![](media/image284.png)

　　務必記得自己移動幾次，或是隨時存檔。

　　請勿將錯誤位置存檔，還原過程較為繁雜，若需進行大範圍調整，請準備好備份檔。

![](media/image221.png)

![](media/image13.png)

操作範例：站點密集應對方式

![](media/image244.png)

站點過於密集：

　　當站點過於密集時，可能導致路徑規劃困難。

![](media/image270.png)

透過座標修改移動站點：

　　使用 X 軸座標修改器（X-Axis） 或 Y 軸座標修改器（Y-Axis） 移動站點，務必記得移動多少次。

![](media/image170.png)

移動後進行路徑連線（Connect Paths After Moving）：

　　移動站點後，進行路徑連線，確保所有站點都能正確連接。

![](media/image300.png)

　　以此類推，用同樣方式連起所有站點，再將站點復歸原位。

![](media/image308.png)

![](media/image284.png)

　　務必記得自己移動幾次，或是隨時存檔。

　　請勿將錯誤位置存檔，還原過程較為繁雜，若需進行大範圍調整，請準備好備份檔。

操作範例：地圖錯位（Map Misalignment）

![](media/image231.png)

問題描述：

　　當我們在匯入站點路徑時，有可能出現如上圖的狀況，乍看之下沒有問題，但實際在運作時一直出現錯誤。

檢查錯誤訊息：

　　檢查錯誤訊息後，可以發現其實是自走車找不到相關路徑，所以我們回到站點上面去檢查，找到了一個站點如下圖。

![](media/image365.png)

問題站點：

　　我們可以看到被選取的綠色站點移動後是獨立出來的，並未與上下路徑進行連接，所以導致經過的路線中斷，產生錯誤。

正確範例：

　　接下來我們看看正確的範例，應同下圖，每條路徑都連接在該站點上。

![](media/image290.png)

處理步驟：

　　針對此範例，我們該做的處理步驟是，先將錯誤的路徑刪除，重新拉取路徑。

![](media/image221.png)

### 4.10.2 地圖顯示 ( Map Display )

　　在地圖上除了上方的功能列外，尚有幾項功能可進行操作。

![](media/image32.png)

#### 4.10.2.1 方向鍵（Arrow Key）：

　　使用左上方的方向鍵進行地圖移動或進行旋轉。

#### 4.10.2.2 地圖縮放（Map Zoom）：

　　將滑鼠鼠標移至地圖範圍中，使用滑鼠滾輪進行縮放。

　　向上滾為放大，向下滾為縮小。

#### 4.10.2.3 復原（ Undo ）：

　　按下 Ctrl + Z。

#### 4.10.2.4 重做（ Redo ）：

　　按下 Shift + Z。

![](media/image284.png)

操作提醒：

　　了解上方使用操作後，我們知道在使用過程中，新增站點時需要點擊 『站點（Points）』 鈕，直接在地圖上點擊新增。

　　若需要還原上一動可使用 『Ctrl + Z』，或直接按鍵盤 『Delete』 鍵將站點移除，但不建議過度使用 『Ctrl + Z』，避免系統狀態失常。

　　不建議使用拖拉將複數目標圈起，避免系統狀態失常。

　　如當下遭遇無法控制的行為，且編輯內容並不多時，因資訊尚未儲存，可重新整理進行重置。

　　養成完成固定步驟就存檔的習慣，降低未存檔卻檔案遺失的風險。

![](media/image221.png)

###  

### 4.10.3 站點屬性 ( Properties )

　　點擊在地圖上的站點時，右側會出現該站點的 站點屬性（Properties）。

![](media/image272.png)

#### 4.10.3.1 站點 ID（Point ID）：

　　站點 ID 編號，依設備形式不同而有所差異。

#### 4.10.3.2 X 軸座標（X）：

　　站點的 X 軸座標位置。

#### 4.10.3.3 Y 軸座標（Y）：

　　站點的 Y 軸座標位置。

#### 4.10.3.4 角度（W）：

　　自走車在該位置的正面方向（目前系統規定車頭先轉再進行移動），設定時不可為負數，請輸入 0 - 360 之間的值。

#### 4.10.3.5 Z 軸座標（Z）：

　　站點的 Z 軸座標位置。

#### 4.10.3.6 路線（Route）：

　　該欄位對應使用 MR（Mobile Robot）上的哪一個路線地圖（Route Map）。**此設定於建立地圖時選擇，若無特殊需求，此處不需要修改**。

#### 4.10.3.7 路口點（Junction）：

　　自走車快到路口點時會去取得路權。

#### 4.10.3.8 強制停車（Go）：

　　此屬性可強制車子在指定站點停車再開。

#### 4.10.3.9 臨時停車專用（TmpParkOnly）：

　　當此選項打勾時，若 MR 的待命點（Standby Point）有設定該點，該點只會被用於交管避讓等行為，不會被當作長時間停等的待命點。

#### 4.10.3.10 群組（Group）：

　　可以將不同站點視為一體，當在取得路權時需全部取得才能放行。同一站點可以屬於不同的群組，以「\|」符號做分隔。具體設定規則因篇幅較多，詳見 『5.3 群組設計原則 ( Group Define )』。

#### 4.10.3.11 啟用（Enable）：

　　此點是否進行啟用，若不啟用，車子則不會經過該點。

#### 4.10.3.12 上貨里程權重（Unload Order）& 13.下貨里程權重（Load Order）：

　　將原本的 里程權重（Order） 拆分為上貨與下貨，設定值可依順序設定，但設備的設定值一定要大於貨架，例：貨架為 1-10，自走車應為 100-110。

　　**在特定的演算法進行路線規劃時，可以更容易區分與應用。**

#### 4.10.3.14 類型（Type）：

　　站點的類型，現有六種：

充電站（Chargestation）、工作站（Reportpoint）

設備站（Stoplocation）、路口點（Trafficcontrolpoint）

交會點（Connectionpoint）、電池交換站 (Auto Battery Change Station)

#### 4.10.3.15 區域 (Zone)：

　　可選取 區域管理 (Zone Management) 所設定的區域項目。

#### 4.10.3.16 站點埠口（Ports）：

　　站點的位置為獨立 ID，但可使用命名標識系統去增加多個 ID 進行標識編號。

　　例如：充電站為 C + 編號，第一座充電站為 C1。

##### 4.10.3.16.1 命名標識系統：

　　此段落在 Port ID 下方的原因是為了更讓使用者清楚其中的關係，我們可以知道每一個站點都有自己的 Port ID 。但當它自己有其他的用途時，就需要增加別名，以利於系統辨識。

　　我們會在 4.10.3.16.9 新增屬性（Add Property）中進行統一說明。

　　例：貨架為 E + 編號 + P + 編號，第二座貨架第五個儲位則為 E2P5。此點設定值為自走車搬運或物所辨識的值，此命名規則可能會視情況進行變動。

　　填寫完畢後點擊加號，就會新增一項在下方，如 EW-2001。

![](media/image46.png)

　　例：避車點，可建立 『AltPointID』，做為指定的避車點。

##### 4.10.3.16.2 鎖頭符號 ( 啟用 / 未啟用 ) ( Lock )：

　　新增預設為勾選啟用，請確認是否打勾啟用 ( Enable )，取消勾選則為 Disable 。

##### 4.10.3.16.3 工作站 ID ( ID )：

　　顯示設定的命名標識 ID。

##### 4.10.3.16.4 E84（e84）：

##### 4.10.3.16.5 CS（CS）：　　

##### 4.10.3.16.6 PN（PN）：

##### 4.10.3.16.7 眼睛符號（Visible / Invisible）：

　　預設為勾選啟用，ID會顯示在地圖上，請確認是否打勾顯示，取消勾選則為 不顯示。

##### 4.10.3.16.8 刪除（Delete）：

　　點擊後刪除該工作站 ID，請記得在 Map 功能項中的 Save 進行存檔，存檔後才會將更改後的參數。

##### 4.10.3.16.9 新增屬性（Add Property）：

　　點擊後會產生空白欄位可進行填寫，剛剛在 4.10.3.16.1 命名標識系統中有大致了解內容，這裡詳細敘述相關功能。

　　點擊 Add Property 時會出現下方的填寫欄位。

![](media/image133.png)

　　下拉選單選項如下：

![](media/image163.png)

- AltPointID：指向要繞至的點位。

- RobotRouteLock：車輛在進行手臂動作時，要鎖路權的點。

- PreProcess、PreProcessParam、PostProcess、PostProcessParam：適用於IoT裝置設定，可見本節之後的參考範例段落。

- Other：視專案使用狀況而定。

　　因各專案自身特性，使用情況較少，如有需求請詢問相關人員。

![](media/image284.png)

**　　※ 命名標識系統的命名概念於整個 TSC 系統中都通用，務必牢記設備的命名規則。**

**　　※ Point ID 與 Ports 的 ID 切記不可重複，否則會造成系統錯誤。**

　　貨架命名依要求有所不同，設備名稱依要求設定。

　　站點屬性中輸入的 Ports 的 ID 是搬移指令會讀取的值。

　　Ports 的 ID 命名方式：

　　　　若為機台： 通常與 Workstation ID 一樣。

　　　　例：OCR01。

　　　　若為充電站： 命名規則建議使用 C + 編號，一般設定為 CX。

　　　　例：第一座充電站為 C1，第二座為 C2，依此類推。

　　　　若為電子貨架： 命名規則建議使用 E + 編號 + P + 編號，一般設定為 EXPX。

　　　　例：第一個貨架的第一個連接埠為 E1P1。

　　　　第二個貨架的第十個連接埠為 E2P10。

　　此點設定值為自走車搬運或物所辨識的值，此命名規則可能會視情況進行變動。

若為避車點： 可建立 『AltPointID』，做為指定的避車點，見上方 『4.10.3.16.9 新增屬性（Add Property）』。

　　注意事項：此為系統固定格式，請勿隨意設定，如有需求請與開發團隊討論客製。

![](media/image221.png)

![](media/image409.png)

　　在地圖上點擊 Point 以及 Path 時，都會出現屬性填寫的區塊。

　　

　　在點上設定點的屬性。下拉式選單的選項是 KEY，依專案需求做選擇，Value 為在該點上呼叫的函數或該函數所需傳入的參數。

　　PreProcess：進入該點時所要呼叫的函數。

　　PreProcessParam：該函數所需傳入的參數，注意必須是json格式。

　　PostProcess：離開該點時所要呼叫的函數。

　　PostProcessParam：該函數所需傳入的參數，注意必須是json格式。

　　需要呼叫的函數及其所需要的參數，視專案使用情況而定，如有需求請詢問相關人員。

　　**注意：PreProcessParam、PostProcessParam必須是json格式。**

![](media/image261.png)

### 4.10.4 路徑屬性 ( Route )

![](media/image265.png)

#### 4.10.4.1 路徑 ID ( ID)：

　　路徑的 ID 編號。

#### 4.10.4.2 路徑長度 ( Weight )：

　　兩個站點間的距離。

#### 4.10.4.3 啟用路徑 ( Enable )：

![](media/image389.png)

　　是否啟用，啟用即可通行。

#### 4.10.4.4 群組 ( Group )：

　　群組，可將站點與路徑組成群組，群組間請用 『 \| 』 隔開。

![](media/image85.png)

操作範例：

　　我們將幾個路徑與站點組成群組，並不予以通行，自走車在尋路時便不會加入該站點與路徑，會採取避開的方式去計算路線。

　　路徑是由站點組成，故只選擇路徑群組起來，所屬站點皆屬於該群組，為避免系統發生問題，請先規劃好各站點與路徑所需要的群組命名，也方便管理。

#### 4.10.4.5 線道 ( Road )：

待補充

#### 4.10.4.6 速度 ( Speed )：

　　行經此路段時的速度限制，預設為 100%。

#### 4.10.4.7 動態迴避 ( Dynamic Avoidance )：

　　該路段啟用後，行經該路段時，會採取動態迴避通過，該路線顯示為**虛線**。

![](media/image325.png)

#### 4.10.4.8 允許逆向超車 ( Reverse Overtaking Allowed )：

　　當路線設定為單行道時，假設 MR 需要逆向超車，則需要勾選該設定（特殊需求，需諮詢相關人員）。(單行道與逆向超車請見 5.1.1.7 單行道 (One-Way Path) 與 5.1.1.8 逆向超車功能 (Reverse Overtaking))

#### 4.10.4.9 站點 ID ( Point ID )：

　　路徑的兩端站點 ID，站點資訊如圖所示會分為兩側。

![](media/image415.png)

#### 4.10.4.10 路徑方向 ( Dir )：

　　路徑選項的重要參數，控管此路徑的進出方向，預設值為兩方都為 IN。

雙向通行：

![](media/image118.png)

單向通行：

![](media/image173.png)

#### 4.10.4.11 座標 ( X )：

　　站點的Ｘ座標位置。

#### 4.10.4.12 座標 ( Y )：

　　站點的Ｙ座標位置。

#### 4.10.4.13 兩端站點屬性 ( Point Property )：

![](media/image176.png)

　　可針對該站點設定參數，因專案特性而定，使用情況較少，如有需求請詢問相關人員。

#### 4.10.4.14 增加屬性欄位 ( Add Property )：

　　 點擊時會出現同選取 Point 時的 4.10.3.16.9 新增屬性（Add Property）中的欄位，如果看過該節的參考範例就一定不會陌生。

![](media/image332.png)

　　在線段兩端的點上設定點的屬性。

　　下拉式選單的選項是 KEY，依專案需求做選擇，Value 為在該點上呼叫的函數或該函數所需傳入的參數。

![](media/image254.png)

　　點擊下拉式選單之後發現跟 Point 的下拉式選單有一點不同。

　　PreProcess：進入該線段時所要呼叫的函數。

　　PreProcessParam：該函數所需傳入的參數，注意必須是json格式。

　　PostProcess：離開該線段時所要呼叫的函數。

　　PostProcessParam：該函數所需傳入的參數，注意必須是json格式。

　　需要呼叫的函數及其所需要的參數，視專案使用情況而定，如有需求請詢問相關人員。

![](media/image409.png)

　　先前在 Point 時有看過這個範例，這個同樣在 Path 也能夠使用。

　　

　　在線段上設定點的屬性。下拉式選單的選項是 KEY，依專案需求做選擇，Value 為在該點上呼叫的函數或該函數所需傳入的參數。

　　PreProcess：進入該線段時所要呼叫的函數。

　　PreProcessParam：該函數所需傳入的參數，注意必須是json格式。

　　PostProcess：離開該線段時所要呼叫的函數。

　　PostProcessParam該函數所需傳入的參數，注意必須是json格式。

　　需要呼叫的函數及其所需要的參數，視專案使用情況而定，如有需求請詢問相關人員。

　　**注意：PreProcessParam、PostProcessParam必須是json格式。**

![](media/image261.png)

### 4.10.5 現有站點列表 ( Points )

![](media/image210.png)

#### ![](media/image64.png)

　　點擊 Point 可以打開列表，地圖上的所有站點都會在此，勾選後該站點會在地圖上隱藏起來，方便進行辨識或連結路徑等操作，操作完畢後儲存即可，不會作為隱藏站點屬性進行儲存。

## 4.11 自走車看板（ Vehicle Dashboard）

![](media/image76.png)

### 4.11.1 TSC 控制列 ( TSC Control )：

![](media/image427.png)

#### 4.101.1.1 TSC 程式運行狀態（TSC Program Status）：

##### 4.11.1.1.1 TSC 啟動中（TSCInitiated）：

　　TSC 啟動時的初始狀態，如果一直卡在該狀態，通常有異常發生導致無法正確啟動 TSC。

##### 4.11.1.1.2 TSC 暫停中（TSCPaused）：

　　TSC 處於暫停狀態，不會將指令派給 MR。可由 Host 下 Paused 指令或是點選右邊 Pause 按鈕觸發。

##### 4.11.1.1.3 TSC 暫停中（TSCPausing）：

　　由 TSCAuto 轉為 TSCPaused 的中間狀態，當 TSC 收到 Pause 訊號時，會先等當前 MR 執行完身上指令才會進入 TSCPaused，此時的中間狀態即為 TSCPausing。

##### 4.11.1.1.4 TSC 自動運行中（TSCAuto）：

　　正常執行指令及運行的狀態。

##### 4.11.1.1.5 TSC 離線中（TSCOffline）：

　　當 TSC 與前端 UI 斷線時，UI 顯示之狀態，該狀態下於 UI 上操作可能無法正確將訊號傳送給 TSC，並且大概率會伴隨操作卡頓。但此狀態不會影響 TSC 及 Host 之間通訊以及搬運指令的執行。

#### 4.11.1.2 TSC 與 Host 之間的底層通訊（TSC-Host Communication）：

##### 4.11.1.2.1 未通訊中（NOT_COMMUNICATING）：

　　TSC 與 Host 之間沒有連線。

##### 4.11.1.2.1 通訊中（COMMUNICATING）：

　　TSC 與 Host 之間通訊正常。

#### 4.11.1.3 TSC 與 Host 之間的控制狀態（TSC-Host Control Status）：

##### 4.11.1.3.1 線上遠端控制中（ONLINE_REMOTE）：

　　TSC 與 Host 之間可以正確傳遞所有 event 及指令。

##### 4.11.1.3.2 Host 離線中（HOST_OFFLINE）：

　　Host 透過指令告知 TSC 下線。

4.11.1.3.3 設備離線中（EQUIPMENT_OFFLINE）：

　　透過右邊 Control Offline 按鈕主動將 TSC 下線。

![](media/image284.png)

　　 當狀態處於 HOST_OFFLINE 及 EQUIPMENT_OFFLINE 將不會發送 event 給上位系統，及接收指令。

![](media/image221.png)

### 4.11.2 地圖顯示頁面 ( Map Display )：

![](media/image266.png)

　　顯示自走車即時運行狀態，可在其顯示區塊按住滑鼠拖移地圖，滾動滑鼠滾輪進行縮放。

![](media/image263.png)

　　右上角功能鍵可恢復顯示比例 『重置鈕（Reset Zoom）』，或是進行視窗的放大。

![](media/image166.png)

　　左上角為顯示點位的數量跟路徑的數量。

#### 4.11.2.1 點位操作 (Nodes Actions)：

　　點擊點位時會出現彈跳視窗，可進行操作。

![](media/image213.png)

　　啟用、禁用點位（Set Node）：送出後將啟用或禁用點位。

![](media/image333.png)

　　派送自走車至點位（Send Vehicle to Node）：呼叫自走車至該點位，暫無功用。

#### 4.11.2.2 路徑操作 (Path Actions)：

　　點擊路徑時會出現彈跳視窗，可進行操作。

![](media/image310.png)

　　啟用、禁用路徑（Set Edge）：送出後將啟用或禁用點位。

![](media/image431.png)

### 4.11.3 自走車選單 ( AMR List )：

![](media/image87.png)

　　目前上線運行的自走車代號都可透過下拉選單進行選取，被選擇的自走車詳細資訊與功能則會顯示在下方。

### 4.11.4 自走車命令選項 ( AMR Control )：

![](media/image236.png)

　　目前命令選項共有四項：

> 充電（Charge）：
>
> 　　命令自走車回到充電站充電。
>
> 模擬（Assert）：
>
> 　　模擬上位系統回覆命令（測試用）。
>
> 清掃（Sweep）：
>
> 　　將自走車上的載具自動放回預設貨架（Fault Erack）。
>
> 手動模式（Manual）：
>
> 　　將自走車改為手動測試模式。

### 4.11.5 自走車任務狀態 ( Task )：

![](media/image96.png)

　　點擊 加號（+） 時會展開表格：

　　　　若該自走車處於 待機狀態（Idle），表格內容為空白

![](media/image120.png)

　　若該自走車處於 運行中（In Operation），則顯示以下資訊：

　　　　命令 ID（ID）

　　　　當前動作（Action）

　　　　載具 ID（Carrier ID）

　　　　目的地（Target）

### 4.11.6 自走車車輛狀態 ( Vehicle Status )：

![](media/image16.png)

#### 4.11.6.1 自走車狀態列表 ( Vehicle Status List)：

　　顯示連線 ( True ) 或未連線 ( False ) 。

#### 4.11.6.2 自走車狀態列表 ( Vehicle Status List)：

| 獲取貨物中（Acquiring） | 機械臂正在抓取載具（Carrier） |
|----|----|
| 充電中（Charging） | 位於充電站進行自主充電 |
| 放置貨物中（Depositing） | 正在工作站或電子貨架（Erack）卸放載具（Carrier） |
| 尋路中（Enroute） | 依規劃路徑移動至目標站點 |
| 停靠中（Parked） | 已抵達指定待命點（Standby Station） |
| 暫停（Pause） | 手動暫停或系統保護性停止 |
| 斷線（Removed） | 與控制系統（TSC）失去通訊連結 |
| 空閒中（Unassigned） | 可立即接受新任務的待命狀態 |
| 載貨請求中（TrLoadReq） | 等待上位系統回覆載貨指令 |
| 卸貨請求中（TrUnloadReq） | 等待上位系統回覆卸貨指令 |
| 電池交換中（Exchanging） | 與自動電池更換系統（ABCS）進行電池置換 |
| 指令待命中（Waiting） | 完成當前任務後等待新指令 |
| 緊急避難中（Evacuation） | 觸發安全協議後的緊急移動狀態 |
| 貨物平移中（Shifting） | 在站區內進行橫向貨物調整 |
| 暫停待機中（Suspend） | 系統指令下的臨時停靠 |

#### 4.11.6.3 移動狀態（Move Status）：

　　反映自走車當前的行動狀況，狀態內容視專案而有不同，請與相關人確認。

#### 4.11.6.4 機械臂狀態（Robot Status）：

　　整體運作模式與位置資訊，狀態內容視專案而有不同，請與相關人確認。

#### 4.11.6.5 電壓檢測（Voltage）：

　　自走車動力系統電壓。

#### 4.11.6.6 電流檢測（Current）：

　　即時電力消耗狀況。

### 4.11.7 自走車錯誤狀態與版本資訊 ( Message )：

![](media/image207.png)

#### 4.11.7.1 訊息顯示 (Message)：

　　顯示當前自走車目前狀態、系統通知或錯誤警報。

#### 4.11.7.1 所在站點 (Station)：

　　當前停靠或作業中的工作站編號。

#### 4.11.7.1 位置點 (Point)：

　　精確座標點位 (對應地圖系統)。

#### 4.11.7.1 電池狀態 (Battery)：

　　當前電量與健康度。

#### 4.11.7.1 健康狀態 (Health)：

　　設備綜合診斷狀態。

### 4.11.8 自走車儲位狀態 ( Ports )：

![](media/image235.png)

#### 4.11.8.1 自走車儲位狀態 ( Ports )：

　　依自走車型號顯示不同儲位數量，以及顯示當前自走車上的 載具 ID ( Carrier ID)。

### 4.11.9 自走車定位姿態 ( Pose )：

![](media/image395.png)

#### 4.11.9.1 X軸座標 (X)：

　　當前水平位置 (車體中心基準)。

#### 4.11.9.2 Y軸座標 (Y )：

　　當前垂直位置 (車體中心基準)。

#### 4.11.9.3 旋轉角度 (W )：

　　車體朝向角度 (0度為正東方向)。　　

#### 4.11.9.3 高度參數 (Z )：

　　待確認。

### 4.11.10 自走車相機 ( Camera )：

![](media/image281.png)

　　有四個相機，前視相機 (Front)、右側相機 (Right)、左側相機 (Left)、後視相機 (Back)。

　　點擊時會開啟新視窗，連向該自走車的鏡頭 IP，進行影片串流。

## 4.12 自走車管理（ Vehicle Management）

### 4.12.1 自走車管理列表 ( AMR Manage )

![](media/image67.png)

　　自走車管理列表中，我們可看到上圖一筆資料是一輛自走車，平值只顯示綠色區塊，當我們點擊該筆資料，就可以打開該輛自走車的充電設定，為紅色區塊，

　　現在我們來說明每一個欄位的內容。

#### 4.12.1.1 自走車資訊 ( 綠色區塊 )：

##### 4.12.1.1.1 自走車 ID (Vehicle ID)：

　　每台自走車的唯一識別編號。

##### 4.12.1.1.2 網路通訊IP位址 (IP)：

　　自走車的網路通訊位址。

##### 4.12.1.1.3 通訊連接埠號 (Port)：

　　與控制系統通訊的埠號。

##### 4.12.1.1.4 指定充電站位置 (Charge Station：

　　自走車的專屬充電站編號。

##### 4.12.1.1.5 預設運作樓層 (Default Floor)：

　　開機後自動回歸的作業樓層。

##### 4.12.1.1.6 服務區域範圍 (Service Zone)：

　　允許運行的區域代碼。

##### 4.12.1.1.7 待命點位置 (Standby Station)：

　　任務間隙的待命位置。

##### 4.12.1.1.8 緊急避難站點 (Evacuate Station)：

　　緊急狀況的避難位置。

##### 4.12.1.1.9 載貨異常處理貨架 (Load Fault Erack)：

　　載貨失敗時的暫存貨架。

##### 4.12.1.1.10 卸貨異常處理貨架 (Unload Fault Erack)：

　　卸貨失敗時的暫存貨架。

##### 4.12.1.1.11 車輛型號規格 (Model)：

　　自走車的硬體型號。

##### 4.12.1.1.12 是否啟用緩衝區功能 (EnableBuffer)：

　　啟用/停用任務緩衝區。

##### 4.12.1.1.13 緩衝區類型設定 (Buffer Type)：

　　緩衝區的工作模式。

##### 4.12.1.1.14 最大運行速度 (Max Speed)：

　　允許的最高移動速度。

##### 4.12.1.1.15 機械臂操作逾時時間 (Robot Timeout)：

　　單次操作最長等待時間。

##### 4.12.1.1.16 呼叫支援延遲時間 (Call Support Delay)：

　　異常呼叫間隔時間。

##### 4.12.1.1.17 任務優先權等級 (Priority)：

　　任務派發優先順序。

##### 4.12.1.1.18 連線重試次數 (Connect Retry)：

　　通訊失敗重試次數。

##### 4.12.1.1.19 是否啟用起始標記 (Enable Begin Flag)：

　　<span class="mark">是否啟用移位退站。移位退站屬於安全機制，讓自走車在離開工作站時進行適當距離的位移，再前往下一個任務站點，請依現場需求再進行勾選，一般預設為不勾選。</span>

##### 4.12.1.1.20 是否允許追加任務 (Append Transfer Allowed)：

　　允許動態新增任務。

##### 4.12.1.1.21 追加任務演算法 (Append Transfer Algo)：

　　任務追加的邏輯規則。

##### 4.12.1.1.22 是否執行載具類型檢查 (Carrier Type Check)：

　　載具相容性檢查。

##### 4.12.1.1.23 是否啟用車輛 (Enable)：

　　自走車運作狀態。

##### 4.12.1.1.24 編輯功能 (Action)：

　　可編輯、刪除此自走車。

#### 4.12.1.2 自走車充電資訊 ( 紅色區塊 )：

##### 4.12.1.2.1 自動充電 (Auto)::

　　是否啟用自動充電功能。

##### 4.12.1.2.2 每趟充電 (Every Round):

　　每次完成任務後是否強制充電。

##### 4.12.1.2.3 最短充電時間 (Minimum Time):

　　每次充電的最短時間。

##### 4.12.1.2.4 低電量閾值 (Below Power):

　　觸發自動充電的電量百分比。

##### 4.12.1.2.5 最低電量運行 (Run After Minimum Power):

　　允許在最低電量下繼續運行。

##### 4.12.1.2.6 閒置時充電 (When Idle):

　　無任務時是否自動充電。

##### 4.12.1.2.7 進入閒置時間 (Into Idle Time):

　　無任務多久後視為閒置。

##### 4.12.1.2.8 電池高電量 (Battery High Level):

　　充電至多少百分比停止。

##### 4.12.1.2.9 充電安全檢查 (Charge Safety Check):

　　充電前執行安全檢測。

##### 4.12.1.2.10 最長充電時間 (Max Time):

　　單次充電最長時間。

##### 4.12.1.2.11 電壓範圍 (Voltage (Min / Max)):

　　允許的充電電壓範圍。

##### 4.12.1.2.12 電流範圍 (Current (Min / Max)):

　　允許的充電電流範圍。

##### 4.12.1.2.13 排程充電 (Schedule Charging):

　　啟用固定時段充電。

##### 4.12.1.2.14 排程充電時間 (Schedule Charging Time):

　　指定充電時段。

##### 4.12.1.2.15 停靠充電 (Park):

　　充電時是否鎖定車輛。

##### 4.12.1.2.16 待命時充電 (When Standby):

　　待命狀態下是否充電。

##### 4.12.1.2.17 進入待命時間 (Into Standby Time):

　　閒置多久後轉為待命。

### 4.12.2 新增自走車 ( Add New Vehicle )

　　資訊列表與新增表單的欄位皆為相同，故可透過下述針對資訊列表的說明，去比對新增自走車的欄位項目，故不贅述。

![](media/image99.png)

#### 4.12.2.1 自走車 ID（Vehicle ID）：

　　自走車的名稱。

#### 4.12.2.2 IP 位址（IP）：

　　自走車連線的 遠端 IP 位置（Remote IP Address）。

#### 4.12.2.3 連接埠（Port）：

　　自走車連線的 遠端連接埠（Remote Port）。

#### 4.12.2.4 機器人超時（Robot Timeout）：

　　可設定 MR 手臂動作後多久沒執行完會觸發警報（Alarm）。

　　例如：當設定為 720 秒，若手臂開始動作後因推車觸發 MR 的 LiDAR 導致手臂暫停，超過 720 秒時便會觸發警報。

#### 4.12.2.5 呼叫支援延遲（Call Support Delay）：

　　MR 可以透過區域（Zone）來設定主要及支援的區域。但如果故障的 MR 馬上就能復原，不希望立即進行支援，可以設定此參數，系統會等時間到之後才進行支援動作。

#### 4.12.2.6 優先度（Priority）：

　　可以針對 MR 設定優先度。當遇到路口交管等情況，優先度高的 MR 會先行通過。

#### 4.12.2.7 裝貨異常貨架（Load Fault Erack）& 卸貨異常貨架（Unload Fault Erack）：

　　自走車發生異常時，會將殘貨送至哪個貨架。

　　　　**注意：為避免系統出現問題，請至少填寫一個電子貨架。**

#### 4.12.2.8 最大速度（Max Speed）：

　　最大速度，建議設定到 500，單位是（ mm/s）。

#### 4.12.2.9 重新連線次數（Connect Retry）：

　　重新連線次數限制。

#### 4.12.2.10 服務區域（Service Zone）：

　　自走車的工作區域，使用 區域管理（Zone Management） 的選項，將自走車安排在相關區域執行工作。負責區域與支援區域之間請用 半形逗號（Comma） 分開。

　　<span class="mark">範例情境：</span>

|  | <span class="mark">A 自走車</span> | <span class="mark">B 自走車</span> | <span class="mark">C 自走車</span> | <span class="mark">D 自走車</span> |
|----|----|----|----|----|
| <span class="mark">負責區域</span> | <span class="mark">zone1</span> | <span class="mark">zone1</span> | <span class="mark">zone2</span> | <span class="mark">zone2</span> |
| <span class="mark">支援區域</span> | <span class="mark">zone2</span> | <span class="mark">zone2、zone3</span> | <span class="mark">zone1</span> | <span class="mark">zone1、zone3、zone4</span> |
| <span class="mark">狀態</span> | <span class="mark">工作滿載</span> | <span class="mark">充電中</span> | <span class="mark">待命中</span> | <span class="mark">閒置 ( Idle )</span> |
| <span class="mark">欄位寫法</span> | <span class="mark">zone1,zone2</span> | <span class="mark">zone1,zone2\|zone3</span> | <span class="mark">zone2,zone1</span> | <span class="mark">zone2,zone1\|zone3\|zone4</span> |

　　當搬運指令累積到一定數量，系統會整理為 批次命令（Batch Commands） 進行工作分配。

　　例如：今天 A 自走車（AMR A） 負擔的工作數量已滿載，而負責相同區域的 B 自走車（AMR B） 正在充電。

　　此時，設定為 zone1 支援區域（Support Zone 1） 且狀態處於 待命（Standby） 與 閒置（Idle） 的 C 自走車（AMR C） 就會收到系統命令，前往進行支援。

#### 4.12.2.11 預設樓層（Default Floor）：

　　當地圖中存在多樓層時，可以透過該欄位決定自走車屬於哪一樓層。

#### 4.12.2.12 充電站（Charge Station）：

　　下拉選項，選擇此自走車屬於哪個充電站，選項來自我們在地圖上新增的充電站。

![](media/image9.png)

#### 4.12.2.13 待命點（Standby Station）：

![](media/image406.png)![](media/image367.png)

　　此項目是自走車（AMR）回去的待命位置。

　　這項功能較為特別，是一個 可複數選擇的下拉選單。

　　新增方式：先透過下拉選單選定選項，再點擊 綠色加號進行新增。刪除方式：同樣需要透過下拉選單選定後，再點擊 紅色減號進行移除。

　　**如何新增待命點（Standby Station）：**

　　Step 1 初始狀態：待命站點列表為空。

![](media/image22.png)

　　Step 2 點開選單：點擊下拉選單，查看可選的站點。

![](media/image122.png)

　　

　　Step 3 選取項目：此處選定 C1。

![](media/image6.png)

　　Step 4 點擊綠色加號加入：點擊 綠色加號，將選定的站點加入待命站點列表。

![](media/image323.png)

　　**如何移除待命點（Standby Station）：**

　　Step 1 選取欲移除多餘項目：此處選定 E2P1。

![](media/image88.png)

　　Step 2 點擊紅色減號移除：點擊 紅色減號，將選定的站點從待命站點列表中移除。

![](media/image233.png)

![](media/image13.png)

　　此處內容較多，請詳讀以了解使用原理。

　　**範例情境一：一般使用**

　　自走車需要臨時停車時，會依照設定上的選項進行尋找停靠。

　　請依現場停車站規劃，為每輛自走車在負責區域設定需要的停車位置。

![](media/image37.png)

　　例如：停車點設定為 E2P1, E2P2, E2P3。

　　當自走車遇到狀況時，會先尋找 E2P1 站點是否可停，若可則進行停靠，若否則尋找 E2P2 是否可停，依此類推。

　　**範例情境二：趕車系統**

　　自走車系統中除了交管系統外，還有 趕車系統（Priority Passing System），下面說明其執行原理。

　　假設現在的作業區中有 A 自走車和 B 自走車。

![](media/image37.png)

　　B 自走車的 待命點（Standby Station） 中，設定了三個站點：E2P1、E2P2、E2P3。

　　當 A 自走車 接收到大量的工作指令開始奔波，行進中遇到閒置的 B 自走車 擋住通行路徑時：

　　A 自走車會發出指令，讓 B 自走車離開。

　　B 自走車會查看它在 待命點（Standby Station） 中設定的站點，並到設定的站點進行臨時停車，讓出通道給 A 自走車通行。

　　B 自走車如何從三個站點中進行選擇？

　　它會依照順序，先詢問上位系統 E2P1 這個站點是否有空位。

　　若有空位，則前往 E2P1 進行臨時停車。

　　若無空位，則尋找 E2P2，依此類推。

　　若找到最後都沒有站點可供停靠，系統會發出警示，告訴使用者這裡塞車了，需要進行障礙排除。

![](media/image308.png)

#### 4.12.2.14 緊急避難點（Evacuate Station）：

　　當系統觸發緊急狀況（上位系統下達避難指令）時，自走車（MR）會自動導航至設定的避難站點。

> 優先邏輯：
>
> 自動選擇「距離最近」的避難站點，若最近站點不可達，則依序嘗試次近站點。

#### 4.12.2.15 型號（Model）：

　　自走車種類，現有自走車型號選項眾多，一般預設使用 Type A（1 arm, 12 inch buffers x 4），各專案使用車輛請與實際狀況相符。

![](media/image205.png)![](media/image141.png)

　　選擇型號後，預設為該型號所有儲位全部啟用。

　　此功能項目為避免突發情況使用，例如自走車其中一個儲位無法辨識 RFID 時，可先暫時停用，待後續維護時再行處理，不會因為一個儲位無法使用導致整輛自走車停用。

##### 4.12.2.15.1 啟用儲位（Enable Buffer）：

　　MR 可針對每個儲位（Buffer）決定是否啟用。

![](media/image84.png)

> 　　例如：若 buf01 不勾選該選項，則 TSC 派貨時就不會選擇該儲位。

##### 4.12.2.15.2 儲位類型（Buffer Type）：

　　可針對每個儲位（Buffer）設定對應的 載具類型（Carrier Type）。

![](media/image150.png)

> 適用於自走車緩衝區不同的情境，也可用 All 代表支援所有類型，請確認現場專案需求並進行填寫。

#### 4.12.2.16 充電設定（Charge）：

![](media/image386.png)

##### 4.12.2.16.1 自動充電模式 (Auto)：

　　啟用智慧充電排程。

##### 4.12.2.16.2 每趟任務充電 (Every Round)：

　　每次完成搬運任務後自動執行充電程序。

##### 4.12.2.16.3 最低充電時間 (Minimum Charge Time)：

　　單次充電最短持續時間：10秒。

##### 4.12.2.16.4 低電量充電閾值 (Charge Below Power)：

　　當電量低於 30% 時觸發自動充電。

##### 4.12.2.16.5 最低運行電量 (Run After Minimum Power)：

　　電量降至 60% 時仍允許執行任務。

##### 4.12.2.16.6 閒置時充電 (Charge When Idle)：

　　啟用無任務時自動充電功能。

##### 4.12.2.16.7 進入閒置時間 (Into Idle Time)：

　　無任務 30秒 後切換至閒置模式。

##### 4.12.2.16.8 電池充飽上限 (Battery High Level)：

　　充電至 99% 自動停止。

##### 4.12.2.16.9 充電安全檢查 (Charge Safety Check)：

　　啟用充電前安全檢測程序。

##### 4.12.2.16.10 最長充電時間 (Charge Time Max)：

　　單次充電最長限制：7200秒（2小時）。

##### 4.12.2.16.11 最低工作電壓 (Voltage Min)：

　　預設為 30 V。

##### 4.12.2.16.12 最高作電壓 (Voltage Max)：

　　預設為 60 V。

##### 4.12.2.16.13 最低充電電流 (Current Min)：

　　預設為 300 mA。

##### 4.12.2.16.14 最高充電電流 (Current Max)：

　　預設為 1000 mA。

##### 4.12.2.16.15 排程充電功能 (Enable Schedule Charging)：

　　啟用預約時段充電，預設時段為 00:00-00:20。

#### 4.12.2.17 停車設定 (Park)：

![](media/image217.png)

##### 4.12.2.17.1 待命時停車 (Park When Standby)：

　　當自走車進入待命狀態時，自動執行停車程序。

##### 4.12.2.17.2 進入待命時間 (Into Standby Time)：

　　無任務持續 30秒 後切換至待命狀態。

#### 4.12.2.18 路線設定 (Route)：

![](media/image100.png)

##### 4.12.2.18.1 自動重新規劃路線（Auto Rerouting）：

　　當自走車取不到路權時，是否要重新計算路線。

##### 4.12.2.18.2 警告阻塞時間（Warning Block Time）：

　　路權多久取不到的時間。

##### 4.12.2.18.3 僅頭尾站點（From To Only）：

　　TSC 在下移動指令時，只會給頭尾的站點，其餘交由自走車決定。

#### 4.12.2.19 啟用移位退站（Enable Begin Flag）：

　　是否啟用移位退站。

　　移位退站屬於安全機制，讓自走車在離開工作站時進行適當距離的位移，再前往下一個任務站點。請依現場需求再進行勾選，一般預設為不勾選。

　　勾選的話，會在移動指令中多帶一個退站的標誌（Flag），告知自走車執行退站。

#### 4.12.2.20 允許附加搬運（Append Transfer Allowed）：

　　回頭車功能。

　　當自走車於機台抓完貨準備放回電子貨架（Erack）時，若儲位（Buffer）還有剩餘空間，可將等待佇列中單純的下機指令接進來一起執行。

#### 4.12.2.21 載具類型檢查（Carrier Type Check）：

　　是否要檢查儲位（Buffer）上的 載具類型（Carrier Type） 欄位。

#### 4.12.2.22 啟用（Enable）：

　　是否上線。

#### 4.12.2.23 新增自走車按鈕（Add Vehicle）：

　　填寫完資料後，點擊即新增該輛自走車。

## 4.13 電子貨架看板 ( eRack Dashboard )

![](media/image430.png)

### 4.13.1 TSC 控制列 ( TSC Control )：

　　此處也有 TSC 控制列，詳見 4.11.1 TSC 控制列 ( TSC Control )。

### 4.13.2 Carrier ID 搜尋 ( Search Carrier ID )：

![](media/image303.png)

　　輸入想尋找的 Carrier ID 並點擊搜尋後，如果有在電子貨架上，該儲位下方的資訊內容則會進行閃爍。

![](media/image144.png)

### 4.13.3 電子貨架列表 (E-Rack List)：

　　顯示所有已建立的電子貨架（E-Rack），即時監控各貨架狀態與儲位水位。

![](media/image56.png)

### 4.13.4 電子貨架資訊 (E-Rack Detail)：

　　點擊列表後會展開電子貨架的內容。

![](media/image61.png)

#### 4.13.4.1 現場 Erack 畫面 ( Erack Webpage )：

![](media/image262.png)

　　點擊後會開啟新頁面，並顯示該電子貨架的畫面，需要設定網址。

#### 4.13.4.2 儲位資訊( Lot Info )：

![](media/image289.png)

##### 4.13.4.2.1 L1 C4 R1：

　　電子貨架中該儲位的所在位置編號，視電子貨架規格而定，分別代表『行 - 欄 - 列』。

##### 4.13.4.2.2 08C11138：

　　晶圓載具 ID (Carrier ID)，命名方式依各專案設定為主。

##### 4.13.4.2.3 右上角 ✔ ：

　　打勾符號，表示該晶圓載具物料已被品檢確認。

##### 4.13.4.2.4 Lot ID：

　　關聯的生產批次號。

##### 4.13.4.2.5 Queue Time：

　　排隊等待時間。

##### 4.13.4.2.6 Next Stage：

　　下一站目的地。

##### 4.13.4.2.7 Description：

　　任務描述資訊。

##### 4.13.4 電子貨架狀態 (E-Rack Status)：

| ![](media/image257.png) | 黑色提示代表該儲位為空。 |
|----|----|
| ![](media/image347.png) | 該儲位的晶圓載具中有物料。 |
| ![](media/image228.png) | 黃色提示代表該儲位的RFID偵測錯誤，或是晶圓載具沒放好。 |
| ![](media/image382.png) | 灰白提示代表該儲位與電子貨架未連線。 |
| ![](media/image377.png) | 綠色提示代表該儲位的晶圓載具即將被自走車載走。 |
| ![](media/image374.png) | 鎖頭符號表示該儲位已被 註冊( Book )，註冊後會變紫色提示，會等待自走車來將它負責運送的晶圓載具送到這個儲位。 |

## 4.14 電子貨架管理 ( eRack Management )

　　進入 電子貨架管理（eRack Management） 後，有四個頁籤：

> 　　匯入電子貨架（Import eRack）
>
> 　　新增電子貨架（Add eRack）
>
> 　　分區管理（Sector Management）
>
> 　　載具管理（Carrier Management）

### 4.14.1 匯入電子貨架( Import Racks )

![](media/image299.png)

操作步驟：

1.  透過點擊 選擇檔案（Choose a File）按鈕，選取檔案匯入 CSV 檔來添加貨架。

2.  如果選錯讀取的檔案，可點擊 清除（Clear）按鈕 清除表單。

3.  若確認檔案內容正確，想匯入時，點擊 匯入（Import）按鈕 進行匯入。

4.  若無現有檔案，可點擊 產生範例檔（Generate）按鈕，系統會產生一個範例 CSV 檔。打開檔案後，依照格式填寫完畢並儲存，再依照剛才說的流程選取檔案進行匯入。

操作建議：

　　這裡我們有範例檔案可以進行測試，但還是建議能夠手動新增一次，以加深對系統的了解。

### 4.14.2 手動添加貨架( Add Rack )

![](media/image419.png)

#### 4.14.2.1 設備 ID（Device ID）\*必填項目：

　　此處指電子貨架 ID，結尾應為數字，命名方式依專案不同而有變化，請與相關人員討論。

　　例如：ER-A01、ER-B01，ER 是 eRack 的簡稱，後為區域與編號。

#### 4.14.2.2 群組 ID（Group ID）\*必填項目：

　　結尾應為數字，當一個區域需要一個以上的電子貨架時，可以將複數的電子貨架編為群組進行使用，並給予一個群組 ID。　　命名方式請與相關人員討論。

　　例如：ER-A、ER-A2，ER 是 eRack 的簡稱，後為區域與群組編號。

#### 4.14.2.3 位置（Location）\*必填項目：

　　電子貨架所在位置，通常為樓層或區域的代稱，命名規則請與相關人員討論。

#### 4.14.2.4 電子貨架設備識別碼（MAC Address）\*必填項目：

　　此處請確認現場設備的 MAC Address，若不知道該設備的 MAC Address，可先填寫代號或是 None。

#### 4.14.2.5 貨架流水編號（Serial Number）\*必填項目：

　　貨架的序列編號，供使用者確認使用。

#### 4.14.2.6 IP 位址（IP Address）\*必填項目：

　　電子貨架的 遠端 IP 位置（Remote IP Address），未正確填寫除無法新增外，亦無法連上電子貨架或模擬器，造成警示錯誤。

#### 4.14.2.7 連接埠（Port）\*必填項目：

　　電子貨架的 遠端連接埠（Remote Port），未正確填寫除無法新增外，亦無法連上電子貨架或模擬器，造成警示錯誤。

#### 4.14.2.8 貨架功能選項（Function）\*必填項目：

　　預設為所有選項未勾選，請依需求選擇，目前功能尚未開放，不勾選即可，如有需求，請與相關人員討論。

> 　　LotIn： 功能保留
>
> 　　LotOut： 功能保留
>
> 　　ECIn： 功能保留
>
> 　　ECOut： 功能保留
>
> 　　Fault： 功能保留

#### 4.14.2.9 樓層（Floor）\*必填項目：

　　電子貨架所在的樓層地圖檔，預設選擇第一個選項，檔案來源為 地圖管理（Map Management）。

#### 4.14.2.10 區域（Zone）\*必填項目：

　　電子貨架在哪個自走車工作區域，資料來源為 區域管理（Zone Management）。

#### 4.14.2.11 型號（Model）\*必填項目：

　　一般貨架請選擇 Shelf，其餘選項為特殊貨架（如旋轉貨架、它廠貨架等），無特殊需求請勿選擇。

#### 4.14.2.12 有效儲位類型（Valid Slot Type）\*必填項目：

　　如果貨架有 載具類型（Carrier Type） 限制，則需設定該欄位。假設整個貨架都是一樣的類型，可以只輸入類型。但如果貨架中有不同的類型，則需要輸入對應儲位。

　　例如：'8S':\[1,2,3,4,5,6\], '12S':\[7,8,9,10,11,12\]。

#### 4.14.2.13 樓層（Floor）\*必填項目：

　　當地圖中存在多樓層時，可以透過該欄位選擇該電子貨架屬於哪一樓層。

#### 4.14.2.14 連結（Link）\*必填項目：

　　原本指令屬於哪個區域（Zone）會依據貨架設定中的 Zone 當作判斷，但因應客戶需求新增該欄位。

#### 4.14.2.15 電子貨架尺寸（Size）\*必填項目：

　　採手動輸入，預設 3x4。如有客製選項需求請與相關人員回報。

#### 4.14.2.16 分區群組（Sector）非必選項目：

　　這裡是較新的內容，說明的部分請見後面章節。

若在 區域管理（Zone Management） 有進行 Sector 分類的設定，在此處就可進行選擇分類，並填上你想要歸類至該分類的儲位編號。

![](media/image238.png)

![](media/image351.png)

#### 4.14.2.17 高水位（Water Level High）：

　　可設定多少百分比為貨架高水位。

#### 4.14.2.18 低水位（Water Level Low）：

　　可設定多少百分比為貨架低水位。

#### 4.14.2.19 水位警報（Alarm for Water Level）：

　　依據上述的設定，可上報警報（Alarm）至上位系統。

> 　　Empty： 空
>
> 　　Low： 低於 Water Level Low 設定值
>
> 　　High： 高於 Water Level High 設定值
>
> 　　Full： 滿水位時

#### 4.14.2.20 啟用（Enable）非必選項目：

　　是否上線，採用勾選方式選擇，預設為未勾選，待實體機台設定完畢或模擬器設定完畢後再行勾選較好。

#### 4.14.2.21 自動派送（Auto Dispatch）：

　　當貨架水位高於 Water Level High 時，是否自動產生自動搬運的指令，從貨架到其他貨架。

#### 4.14.2.22 批次大小（Batch Size）：

　　如果滿足自動搬運條件的話，一次要搬幾筆。

#### 4.14.2.23 返回至（Return To）：

　　搬至哪一個貨架。

　　確認輸入完畢後，因為模擬器還沒開啟，電子貨架啟用（Enable）先不點選，點擊 新增（Add）。

![](media/image134.png)

　　新增完電子貨架後，會出現在下方 電子貨架管理列表（eRack Management List）。

![](media/image73.png)

　　這時我們可以點開 電子貨架看板（eRack Dashboard），未啟用的電子貨架會呈現灰白的狀態。

### 4.14.3 分區管理（Sector Management）

![](media/image369.png)

　　可依照需求將現有的 電子貨架 (Erack) 進行分區，無視貨架的區分，規劃在指定分區內的儲位都可提供給設定的任務進行使用。

#### 4.14.3.1 新增分區 (Add Sector)：

　　輸入分區名稱並點擊新增，則可新增分區，分區命名請與相關人員確認。

Sector範例:{"HOLD_LOT":"1,2,3,4,5,6,7,8,9"}，HODL_LOT是dest port，1~9是順序

特殊符號都要照範例打才會生效

#### 4.14.3.2 全部儲存 (Save All)：

　　重要的功能按鈕，務必在執行任何動作後進行儲存。

#### 4.14.3.3 分區列表 (Sectors)：

##### 4.14.3.3.1 分區名稱 (Sector Name)：

　　設定區域的識別名稱。

##### 4.14.3.3.2 區域顏色 (Sector Color)：

　　選擇區域在介面上的顯示顏色。

##### 4.14.3.3.3 高水位設定 (Water Level High)：

　　觸發高水位警報的臨界值。

##### 4.14.3.3.4 低水位設定 (Water Level Low)：

　　觸發低水位警報的臨界值。

##### 4.14.3.3.5 水位警報 (Alarm for Water Level)：

　　啟用水位異常警示功能。

##### 4.14.3.3.6 動作設定 (Action)：

　　僅有刪除按鈕，需要修改時請刪除後重新新增。

### 4.14.4 載具管理（Carrier Management）

![](media/image116.png)

　　此頁籤的用途是管理專案所使用的載具類別，即 Carrier Type，請依照各專案所需要用到的項目進行設定。

#### 4.14.4.1 選擇檔案 (Choose a file)：

　　點擊此按鈕可從本機電腦選取要上傳的檔案，支援格式 csv 檔。

![](media/image215.png)

　　選擇檔案後會直接引入資料。

#### 4.14.4.2 產生範例檔案 (Generate Example file)：

　　系統會自動下載一個標準格式的範本檔案，初次使用時了解檔案格式，或需要批量新增資料時作為參考。

#### 4.14.4.3 清除 (Clear)：

　　清空目前已選擇的檔案與引入內容。

#### 4.14.4.4 匯入 (Import)：

　　將選取的檔案資料匯入系統，系統會進行檔案格式驗證、 資料完整性檢查、 重複資料提示等檢查。

#### 4.14.4.5 匯出 (Export)：

　　將當前載具資料匯出為檔案。

## 4.15 物聯網設備管理 ( IOT Device Management )

![](media/image336.png)

### 4.15.1 物聯網設備列表 ( IOT Device List )

　　欄位由左至右說明如下：

#### 4.15.1.1 控制設備 (Controller)：

　　此裝置所屬的控制設備。

#### 4.15.1.2 裝置 ID (Device ID)：

　　裝置的唯一識別碼，格式理論上為英數字組合，視各專案而定，請詢問相關人員。

#### 4.15.1.3 裝置類型 (Device Type)：

　　該裝置所屬的類型分類，因設備繁多，針對各 IOT 設備的類型代號，請詢問相關人員。

#### 4.15.1.4 裝置型號 (Device Model)：

　　同裝置類型，該裝置的型號依現場設備而定，請詢問相關人員。

#### 4.15.1.5 IP 位址 (IP)：

　　可連上該裝置的網路位址。

#### 4.15.1.6 通訊埠 (Port)：

　　該裝置的通訊埠號。

#### 4.15.1.7 重試次數 (Retry Time)：

　　通訊失敗時的自動重試次數，依專案與現場狀況而定。

#### 4.15.1.8 通訊逾時 (Socket Timeout)：

　　等待裝置回應的時間（秒）。

#### 4.15.1.9 通訊類型 (Comm Type)：

　　選擇通訊協定：目前有 restful 跟 socket 兩種。

#### 4.15.1.10 狀態 (Status)：

　　顯示裝置當前狀態。

#### 4.15.1.11 啟用 (Enable)：

　　開關控制是否啟用此裝置，預設值為未啟用。

#### 4.15.1.12 操作 (Action)：

　　可執行的管理動作，編輯設備與刪除設備。

### 4.15.2 新增設備 (Add New Device)

![](media/image313.png)

　　因於前一節介紹了全部欄位，故於此處介紹部分可供選擇的項目內容。

4.15.2.1 控制設備 (Controller)：

![](media/image195.png)

　　預設選項為六種，請依專案需求選擇並添加，新增時會因選擇設備不同，需填寫的內容也不相同。

##### 4.15.2.1.1 電池交換站 (ABCS)：

![](media/image135.png)

##### 4.15.2.1.2 電梯控制專用系統 (ELV)：

![](media/image361.png)

##### 4.15.2.1.3 工業烤箱主控制器 (OVEN)：

![](media/image209.png)

##### 4.15.2.1.4 烤箱輔助控制介面 (OVENAdapter)：

![](media/image52.png)

##### 4.15.2.1.5 門禁系統閘道控制器 (GATE)：

![](media/image219.png)

###### 4.15.2.1.5.1 通訊類型 (Comm Type)：

![](media/image350.png)

　　選擇通訊協定：目前有 restful 跟 socket 兩種。

###### 4.15.2.1.5.2 需要登入 (Comm Type)：

　　如該設備需要登入，則須要勾起，並填寫對應的登入 API。

　　可發現此處與其他設備的填寫項目不同，需取得設備的 API 進行發送，如登入、發送指令、連線等 API，故對應的填寫內容請詢問相關人員。

##### 4.15.2.1.6 空間環境控制系統 (CTRLSPACE)：

![](media/image211.png)

　　同　4.15.2.1.5 門禁系統閘道控制器 (GATE)，請詢問相關人員。

### 

### 

### 

### 

###  

### 4.15.3 編輯設備 (Edit Device)

　　與新增設備相同，編輯時會因設備不同，編輯內容也不相同。

##### 4.15.3.1.1 電池交換站 (ABCS)

![](media/image433.png)

##### 4.15.3.1.2 電梯控制專用系統 (ELV)

![](media/image404.png)

##### 4.15.3.1.3 工業烤箱主控制器 (OVEN)

![](media/image190.png)

##### 4.15.3.1.4 烤箱輔助控制介面 (OVENAdapter)

![](media/image40.png)

##### 4.15.3.1.5 門禁系統閘道控制器 (GATE)

![](media/image375.png)

##### 4.15.3.1.6 空間環境控制系統 (CTRLSPACE)

![](media/image82.png)

## 4.16 設備維護 ( Components Maintain )

![](media/image114.png)

　　設備維護管理頁面，目前針對自走車的零組件使用狀態進行設定紀錄。進入此頁面可發現三個區塊，下面依序進行介紹：

### 4.16.1 定期維護排程 (Scheduled Maintenance)：

![](media/image81.png)

　　此項目預設為折疊狀態，點擊加號可展開，做為定時器使用，點擊編輯 ( Edit ) 按鈕後會出現日曆選單。

#### 4.16.1.1 例行性維護 (Routine Maintenance)：

　　按需求進行時間設定。

#### 4.16.1.2 通知時間設定 (Inform Time)：

　　設定維護前的預先通知時間。

#### 4.16.1.3 操作 (Action)：

　　點擊打開時間設定。

![](media/image316.png)

### 4.16.2 自走車零組件用量設定 (Vehicle Component)：

![](media/image394.png)

　　同維修排程，預設狀態為折疊，點擊加號可展開。展開後我們能看到許多欄位，該欄位分別為自走車的電池健康度與四顆輪胎的里程項目。

　　此表為零組件的統合計算表，我們透過下方表格先來了解此表的內容。

| Vehicle ID | 此項為下拉選單，可選擇欲新增零組件規劃的自走車。 |  |  |  |
|----|----|----|----|----|
|  | Serial Number | Installed Time | Upper Limit | Usage Amount |
|  | 零組件序號 | 更換時間 | 使用上限 | 已使用用量 |
| Battery | 請依各項零組件對應編號進行輸入。 | 各項零組件的零件更換時間。 | 此處以充電回數 ( cycle times ) 表示。 |  |
| Left Front Wheel |  |  | 此處以輪胎使用里程表示，單位為公尺 ( m ) 表示。 |  |
| Right Front Wheel |  |  |  |  |
| Left Back Wheel |  |  |  |  |
| Right Back Wheel |  |  |  |  |

#### 4.16.2.1 填寫基本資訊 (Vehicle Components Change Form)：

　　了解了欄位內容後，我們先點擊黃色的 編輯 (Edit) 會出現下列彈跳視窗，依照需求進行填寫。

![](media/image66.png)

　　填寫完畢後點擊藍色的 編輯 (Edit) 進行儲存。

#### 4.16.2.2 用量設定 (Setting Usage Amount)：

![](media/image208.png)

　　點擊此按鈕後會出現下方欄位，請依需求進行填寫。

![](media/image79.png)

　　使用者可透過該選單進行零組件資訊更新，依序輸入序號與零組件的使用上限，設定後會列入當前資訊進行紀錄。

　　每項零組件一旦填寫序號，就必須填寫使用上限，否則無法送出。

![](media/image284.png)

1\. 安裝時間的重要性

　　當您填寫任何一項零組件更換資訊時，必須同時填寫最後一欄的【安裝時間】。這個時間是指：

- 實際更換零件的時間（不是現在填表單的時間）

- 用來準確計算零件使用壽命

- 作為保固期的起始依據

2\. 如何填寫安裝時間

點擊日期欄位：

> 會彈出跟「維修排程」相同的月曆選單
>
> 可以直接選擇年月日

時間精確到小時分鐘：

> 例如：2024年3月15日 下午2點30分
>
> 系統會自動儲存為：2024/03/15 14:30

3\. 為什麼要這樣設計？

> 避免忘記記錄：強制填寫確保每筆更換都有時間紀錄
>
> 維修分析：工程師可以查看：
>
> 哪個零件最容易故障
>
> 平均多久需要更換一次

![](media/image221.png)

### 4.16.3 車輛元件維護歷史 (Vehicle Component History)：

![](media/image297.png)

　　每筆 Log 代表每一次的資料更新內容，會顯示新增的使用者與創建時間，其餘項目與『自走車零組件用量設定 ( Vehicle Component )』相同，SN / UL 是 Serial Number 與 Upper Limit 的縮寫。

##  

## 4.17 帳號管理 ( Account Management )

　　帳號權限管理頁面，可新增、修改、刪除帳號資訊，調整權限範圍。

　　此頁面有三個頁籤，分別如下：

- 使用者管理 ( User Manegement )

- 權限設定 ( Permissions Settings )

- 權限等級 ( Account Type )

### 4.17.1 使用者管理 ( User Manegement )

![](media/image147.png)

#### 4.17.1.1 列表功能 (Options)：

##### 4.17.1.1.1 切換每頁筆數 (Entries Select)：

　　點擊後可切換每頁顯示筆數。

##### 4.17.1.1.2 資料搜尋 (Search)：

　　可輸入關鍵字進行搜尋。

#### 4.17.1.2 使用者管理列表 (User List)：

##### 4.17.1.2.1 登入帳號 (Login ID)：

　　使用者帳號。

##### 4.17.1.2.2 帳號權限類別 (Account Type)：

　　顯示該使用者之帳號權限類別。

##### 4.17.1.2.3 帳號創建時間 (Created At)：

　　顯示該使用者之帳號權限類別。

##### 4.17.1.2.4 編輯功能 (Action)：

###### 4.17.1.2.4.1 編輯 (Edit)：

　　在帳號清單中，點選【編輯 (Edit)】按鈕，系統會顯示「編輯使用者」彈跳視窗。

![](media/image417.png)

可調整項目：

- 顯示名稱 (Name)

- 權限群組 (Account Type)

- 密碼 (Password) 註：輸入新密碼會直接覆蓋舊密碼

- 確認密碼 (Confirm Password)

###### 4.17.1.2.4.2 刪除 (Delete)：

![](media/image428.png)

　　在帳號清單中，點選【刪除 (Delete)】按鈕，系統會顯示「確認刪除」警告視窗。需明確點選【確認 (Confirm)】才會執行刪除

#### 4.17.1.3 重新整理 (Refresh)：

　　重新獲取列表資料。

#### 4.17.1.4 新增使用者 (New)：

![](media/image191.png)

##### 4.17.1.1.1 登入帳號 (Login ID)：

　　使用者帳號，請依方便管理的方式進行設定，勿填寫中文。

##### 4.17.1.1.2 顯示名稱 (Name)：

　　此名稱會顯示在系統介面中（如：儀表板，日誌，操作身份等）。

##### 4.17.1.1.3 登入帳號 (Login ID)：

　　使用者帳號，請依方便管理的方式進行設定，勿填寫中文。

##### 4.17.1.1.4 帳號權限類別 (Account Type)：

　　預設四種權限等級，可自行去帳號權限頁籤進行編輯。

##### 4.17.1.1.5 密碼 (Password)：

　　安全性要求：至少8字元，含大小寫英文與數字，避免使用生日、連續數字（如　123456）。

　　系統不會顯示明文密碼（輸入時會隱藏）。

##### 4.17.1.1.6 確認密碼 (Confirm Password)：

　　需與「密碼」欄位完全一致，防止輸入錯誤，完成後點擊【新增使用者 (Add New User)】按鈕。

##### 4.17.1.1.7 新增使用者 (Add New User)：

　　點擊後則直接新增該使用者。

##### 4.17.1.1.8 取消 (Cancel)：

　　點擊後則取消新增使用者。

### 4.17.2 權限設定 ( Permissions Settings )

![](media/image306.png)

#### 4.17.2.1 權限群組下拉選單 (Group Selection Dropdown)：

　　從下拉選單中選擇目標群組，系統會自動顯示該群組的現有權限設定。

　　**需先選定群組才能編輯權限**，點選【編輯 (Edit)】按鈕進入修改模式。

#### 4.17.2.2 重新整理 (Refresh)：

　　點擊後重新獲取最新權限資訊。

#### 4.17.2.3 編輯權限 (Edit Permissions)：

![](media/image224.png)

　　修改流程：

　　　　① 在目標群組頁面點選【編輯 (Edit)】

　　　　② 透過彈出視窗調整權限：點擊欲更改的權限項目，完成後點擊儲存。

| 等級          | 權限範圍                           |
|---------------|------------------------------------|
| 唯讀（View）  | 僅可瀏覽內容，無法修改             |
| 編輯（Edit）  | 可修改內容，但無法變更系統設定     |
| 管理（Admin） | 完整權限（含參數設定與使用者管理） |

### 4.17.3 權限等級 ( Account Type )

![](media/image307.png)

#### 4.17.3.1 修改帳號群組 (Edit Account Group)

![](media/image222.png)

　　點擊欲修改欄位後，可直接進行編輯，編輯完畢點擊 編輯名稱 (Edit Name) 後進行儲存。

#### 4.17.3.2 刪除帳號群組 (Delete Account Group)

![](media/image292.png)

　　點擊『刪除 ( Delete Account Type )』按鈕，會出現彈跳警告視窗，確定我們是否真的要刪除該帳號群組，點擊確認後就會刪除該帳號群組。

#### 4.17.3.3 重新整理 (Refresh)：

　　點擊後重新獲取最新權限資訊。

#### 4.17.3.4 新增帳號群組 (Add New Account Group)

![](media/image400.png)

　　帳號群組（又稱「帳號類型」或「帳號分類」）主要用於權限管理分類。

　　選【新增 (Add New)】按鈕，系統會顯示「新增帳號群組」彈出視窗。

　　填寫以下欄位：

　　　　New Account Type（群組 ID）：系統辨識用，請使用大寫英文（如 ADMIN），禁止使用中文、空格或特殊符號。

　　　　New Account Name（群組名稱）：✓ 使用者介面顯示用（如業務部、管理組），可依專案需求自由命名。

　　完成後點擊【Add New Account Type】儲存。

　　至 權限設定 (Permissions Settings) 調整該群組的詳細權限。

## 4.18 系統記錄管理 ( Log Management )

![](media/image200.png)

### 4.18.1 時間篩選 (Time Search)：

　　點擊時可選擇日期，篩選期間範圍內的日誌檔案。

### 4.18.2 搜尋 (Search)：

　　可輸入關鍵字進行搜尋，篩選出對應關鍵字的日誌檔案。

### 4.18.3 日誌列表 (Log List)：

#### 4.18.3.1 紀錄 ID (ID)：

　　每筆Log的唯一識別碼。

#### 4.18.3.2 命令 ID (Command ID)：

　　關聯的任務指令編號。

#### 4.18.3.3 任務事件類型選擇 (Select Type)：

　　任務事件的分類標籤，因其項目過多，故使用表格列出。

|  | 中文名稱 | 英文名稱 | 說明 |
|----|----|----|----|
| 1 | 警報 | ALARM | 系統發生嚴重異常或安全機制觸發時記錄 |
| 2 | 載具安裝完成 | CarrierInstalled | FOUP/SMIF盒成功安裝至儲位時觸發 |
| 3 | 載具移除完成 | CarrierRemoved | 載具從儲位被取出時記錄 |
| 4 | 指令編輯更新 | CommandsEditUpdate | 任務指令被手動修改時記錄差異 |
| 5 | 系統異常錯誤 | ExceptionError | 未捕獲的程式例外錯誤資訊 |
| 6 | 手動記錄訊息 | ManualMessage | 操作員手動輸入的備註訊息 |
| 7 | 地圖更新完成 | MapUpdateCompleted | 導航地圖成功更新時觸發 |
| 8 | 空值 | None | 預設值或未分類事件的保留類型 |
| 9 | 資料欄位錯誤 | NoSuchColumnError | 資料庫查詢欄位不存在錯誤 |
| 10 | 並行任務啟動 | Parallel start | 啟用多 AMR 協同作業模式時記錄 |
| 11 | 儲位狀態變更 | SlotChanged | 儲位Occupied/Empty狀態切換時觸發 |
| 12 | 資料庫錯誤 | SQLAlchemyError | 資料庫操作失敗的詳細錯誤 |
| 13 | 儲位-載具對應表更新 | STKCUpdate | 系統載具位置表刷新記錄 |
| 14 | 任務取消完成 | TransferCancelCompleted | 搬運任務被成功中止時記錄 |
| 15 | 任務完成 | TransferCompleted | 搬運任務正常結束的統計資訊 |
| 16 | 執行佇列新增 | TransferExecuteQueueAdd | 任務進入執行階段時觸發 |
| 17 | 執行佇列移除 | TransferExecuteQueueRemove | 任務離開執行佇列時記錄 |
| 18 | 任務格式檢查拒絕 | TransferFormatCheckReject | 任務指令格式錯誤時觸發 |
| 19 | 任務初始化 | TransferInitiated | 新建搬運任務時記錄參數 |
| 20 | 參數檢查拒絕 | TransferParamsCheckReject | 任務參數驗證失敗時觸發 |
| 21 | 任務執行中 | Transferring | 任務進度定期更新的心跳事件 |
| 22 | 等待佇列新增 | TransferWaitQueueAdd | 任務進入排程等待時記錄 |
| 23 | 等待佇列移除 | TransferWaitQueueRemove | 任務離開等待狀態時觸發 |
| 24 | 載貨請求 | TrLoadReq | AMR 發送載貨指令時記錄 |
| 25 | 卸貨請求 | TrUnLoadReq | AMR 發送卸貨指令時觸發 |
| 26 | 交通控制更新 | TSCUpdate | TSC參數被修改時記錄 |
| 27 | 車輛取得完成 | VehicleAcquireCompleted | AMR 成功取得任務時觸發 |
| 28 | 車輛取得開始 | VehicleAcquireStarted | AMR 開始競爭任務時記錄 |
| 29 | 車輛抵達 | VehicleArrived | AMR 到達指定站點時觸發 |
| 30 | 車輛指派 | VehicleAssigned | 任務正式分配至 AMR 時記錄 |
| 31 | 車輛阻塞 | VehicleBlocking | AMR 因障礙物停止移動時觸發 |
| 32 | 充電開始 | VehicleChargeBegin | AMR 開始充電程序時記錄 |
| 33 | 充電完成 | VehicleChargeCompleted | AMR 完成充電時觸發 |
| 34 | 充電結束 | VehicleChargeEnd | 充電程序正常/異常終止時記錄 |
| 35 | 充電啟動 | VehicleChargeStarted | AMR 進入充電站時觸發 |
| 36 | 車輛離開 | VehicleDeparted | AMR 離開站點時記錄 |
| 37 | 放置完成 | VehicleDepositCompleted | AMR 完成載具放置時觸發 |
| 38 | 放置開始 | VehicleDepositStarted | AMR 開始放置載具時記錄 |
| 39 | 車輛初始化 | VehicleInit | AMR 開機完成初始化時觸發 |
| 40 | 車輛安裝完成 | VehicleInstalled | 新 AMR 部署完成時記錄 |
| 41 | 暫停解除 | VehiclePauseClear | AMR 暫停狀態解除時觸發 |
| 42 | 暫停設定 | VehiclePauseSet | AMR 被手動/自動暫停時記錄 |
| 43 | 路徑規劃 | VehicleRoutesPlan | AMR 計算新路徑時觸發 |
| 44 | 車輛解除指派 | VehicleUnassigned | AMR 任務被解除時記錄 |

#### 4.18.3.4 訊息內容 (Message)：

　　Log的詳細描述。

#### 4.18.3.3 日誌狀態選擇 (Select Type)：

![](media/image274.png)

　　Log的狀態分類標籤，當前狀態有四種。

##### 4.18.3.3.1 資訊 (INFO)：

　　記錄系統正常運作狀態。

##### 4.18.3.3.2 警告 (WARNING)：

　　標記潛在異常但未影響運作。

##### 4.18.3.3.3 錯誤 (ERROR)：

　　記錄需立即處理的異常。

##### 4.18.3.3.4 嚴重錯誤 (SERIOUS)：

　　影響系統安全的重大異常。

#### 4.18.3.5 使用者 (User)：

　　操作人員帳號。

#### 4.18.3.5 建立時間 (Created At)：

　　Log產生的時間戳記。

### 4.18.4 重新整理 (Refresh)：

　　點擊後可重新獲取最新的日誌資料。

### 4.18.5 匯出檔案 (Export)：

![](media/image240.png)

　　點擊後可匯出指定時間範圍內的日誌檔案。

## 4.19 系統記錄下載 ( Log Files )

![](media/image128.png)

### 4.19.1 日誌檔案下載 ( Download LogFiles )：

![](media/image408.png)

　　點擊時可選擇日期，下載期間範圍內的日誌檔案。

### 4.19.2 日誌檔案搜尋 ( Search LogFiles )：

　　輸入關鍵字進行日誌搜尋。

### 4.19.3 日誌檔案列表 ( LogFiles List )：

#### 4.19.3.1 檔案名稱 (Filename)：

　　顯示 log 檔案的完整名稱。

#### 4.19.3.2 目錄路徑 (Directory)：

　　顯示 log 檔案存放的絕對路徑。

#### 4.19.3.3 檔案大小 (Size)：

　　顯示 log 檔案的實際大小。

#### 4.19.3.4 最後修改時間 (Last Modified)：

　　顯示檔案最後修改的時間戳記。

#### 4.19.3.5 操作功能 (Action)：

　　提供對 log 檔案的操作選項，下載 (Download) 與 刪除 (Delete)。

### 4.19.4 選擇資料夾 ( Select Folder )：

![](media/image137.png)

　　可選擇對應需求的 Log 資料夾路徑。

### 4.19.5 重新設定 ( Reset )：

　　 點擊後將會回到預設設定，並重新撈取檔案。

### 4.19.6 連結自走車 ( Connect AMR )：

　　跟地圖一樣，需輸入自走車 IP 後進行連結，可獲得該自走車的資料夾路徑。

### 4.19.7 目前所在資料夾 ( Current Folder )：

　　可知道當前資料夾的位置，方便判斷並選取檔案。

### 4.19.8 自走車日誌檔列表 ( AMR Log List )：

　　同 4.19.3 日誌檔案列表 ( LogFiles List )。

# 5. 概念說明

## 5.1 交通管制概念介紹（Traffic Control Concepts）

![](media/image284.png)

**以下幾個概念會出現在我們 TSC 派車系統中。**![](media/image221.png)

### 5.1.1 車輛行車規則（Vehicle Driving Rules）：

#### 5.1.1.1 車輛行車規則（Vehicle Driving Rules）：

　　當自走車想要從一個站點移動到另一個站點時，ACS 系統會從數條可能的路線中，規劃一條最佳路線作為行車路線。（現為最短移動距離為規劃目標。）

##### 5.1.1.1.1 車輛走行 (Vehicle Movement)：

　　自走車的行走方式為：先旋轉至與終點站同方向，再直線移動。

##### 5.1.1.1.2 直行判定 (Straight Movement Judgment)：

![](media/image155.png)

　　當 前一路徑 與 後一路徑 的向量夾角 大於 θ 角度 時，TSC 會將其判定為轉角，並下達 Go 點 指令。

　　當 下一個走行點 的車頭方向與當前不同時，TSC 會將其視為 旋轉點，並下達 Go 點 指令。

##### 5.1.1.1.3 轉彎設定 (Turning Configuration)：

![](media/image148.png)

　　如圖所示，若要規劃一個轉彎處，需在路口處需設置兩個不同方向的點位，此設計可確保自走車在行經路口時能正確執行轉彎動作。

　　實務上，中間的黃色點位通常會重疊在一起，或者非常接近。

#### 5.1.1.2 Keep/Go 點（Keep/Go Points）：

　　下給自走車的點位有兩種屬性，一種是 Keep 點，一種為 Go 點。

　　在給予自走車走行指令的時候，若該站點為 Go 點，自走車會確實走到該點上，再往下走。若該站點為 Keep 點，則自走車會忽略該點直接通過。

　　一般走行邏輯，若接下來自走車車頭方向改變，或者接下來的路徑有一定程度的偏折，則該站點會被運算為 Go 點。

#### 5.1.1.3 路權（Right of Way）：

![](media/image328.png)

　　路權是管理車輛的重要屬性，唯有取得路權的自走車可以通過該站點，確保兩車不會相撞。

　　當自走車要出發前，會先預訂接下來路徑的路權。若出發的路徑路權先被其他自走車佔住，則會等待直到路權能夠被取得。

　　

　　要不到路權時會根據不同情況有不同的決策策略。

![](media/image319.png)

##### 5.1.1.3.1 基本原則 (Basic Principle)：

　　每個站點的通行權限僅允許單一自走車佔用，自走車執行任務前必須取得完整路徑的通行權限，避免碰撞風險。

##### 5.1.1.3.2 路權類型 (Right-of-Way Types)：

　　靜態路權 (Static Right-of-Way)：

- 適用於自走車處於靜止狀態時。

- 系統會將自走車登記在靜態路權清單中。

　　動態路權 (Dynamic Right-of-Way)：

- 自走車移動前需先註冊路徑權限。

- 同時系統會自動註銷該自走車的靜態路權。

##### 5.1.1.3.3 運作流程 (Operation Flow)：

　　當自走車準備移動時：

1.  向系統申請動態路權（包含規劃路徑）。

2.  系統核准後註銷靜態路權。

3.  取得完整路權後開始執行任務。

#### 5.1.1.4 繞路（Detour）：

　　ACS 系統會按照規劃的路線，試著取得該輛自走車自起始位置到下一個路口或目的地上所有節點的獨佔權（即前文 5.1.1.3 路權（Right of Way））。若取得了某節點路權，其他自走車不能路過或停在該點上，這設定是確保行車時不會被其他自走車阻擋。

　　若繞路成功，會將新路線交給自走車，命令該自走車依路線前進。

#### 5.1.1.5 群組（Group）：

![](media/image355.png)

　　規劃走行路徑時，若遇到需要旋轉車頭的情況，或著兩工作站點十分靠近的時候，會需要將該鄰近的點組成一個 Group，避免將其他車派到同樣站點。(同前文 5.1.1.1.3 轉彎設定 (Turning Configuration))

　　如此一來，便有足夠空間進行旋轉或讓路。

##### 5.1.1.5.1 基本概念 (Basic Concept)：

　　系統允許將多個站點劃分為同一個群組，同群組內的所有點位僅允許單一自走車同時佔用。

##### 5.1.1.5.2 群組設計原則 (Group Design Principle)：

> 防護範圍設定：

- 需包含站點前後左右各1個車身距離。

- 需額外加入安全緩衝區範圍。

> 強制群組條件：

- 同一貨架的不同儲位。

- 任何可能造成自走車互相干涉的相鄰站點。

![](media/image226.png)

　　場域中過於靠近的站點(例如同貨架的不同位置)會讓自走車互相干涉，所以必須設為相同的群組。原則上前後左右距離一個車身+防護範圍內的點須確保為同群組。

　　如上圖所示，綠圈範圍內的點應該要屬於同一個群組。

##### 5.1.1.5.3 群組重疊設定 (Group Overlap Configuration)：

![](media/image18.png)

　　單一站點可同時歸屬多個群組，設定語法：使用「\|」符號分隔不同群組名稱。

　　範例：GroupA\|GroupB。

　　運作規則 (Operation Rules)：

1.  佔用狀態：當自走車佔用重疊點位時，所有關聯群組皆視為被佔用，相關群組內所有點位禁止其他自走車進入，

2.  非佔用狀態：當MR僅佔用某群組非重疊點位時。其他群組點位仍可開放使用。

![](media/image416.png)

　　如圖所示，中間的點分別屬於橘色群組與綠色群組。當有一輛自走車在中間時，兩邊的點皆不允許有其他自走車進入。但當自走車停在左邊或右邊的時候，另一邊是可以允許其他自走車進入。

#### 5.1.1.6 車輛優先級(Priority)：

![](media/image152.png)

　　在自走車設定頁面可以設定該車的優先級。優先級小的車輛，在遇到爭道的時候

會主動讓給優先級大的車輛。

#### 5.1.1.7 單行道 (One-Way Path)：

![](media/image413.png)

　　在路徑屬性中設定路徑方向，即可決定該路徑為單行道或雙向道。這項功能幫助使用者根據實際需求，靈活配置車輛的通行方向，確保運作安全與效率。

1.  雙向道 (Two-Way Path)：

> 條件：路徑兩端同時設定為「IN」或同時設定為「OUT」。
>
> 效果：車輛可以雙向通行。

2.  單行道 (One-Way Path)：

> 條件：路徑一端設定為「IN」，另一端設定為「OUT」。
>
> 效果：車輛只能由「IN」端向「OUT」端通行。

3.  觀察箭頭符號：

> 路徑上會顯示箭頭符號，指示車輛的通行方向。
>
> 雙向道：箭頭符號顯示雙向通行。
>
> 單行道：箭頭符號顯示由「IN」到「OUT」的單向通行。

#### 5.1.1.8 逆向超車功能 (Reverse Overtaking)：

![](media/image15.png)

　　當逆向超車功能被打勾後，代表該單行道允許車輛進行逆向超車。這項功能主要用於特殊情況下（如緊急避讓或路徑堵塞），允許車輛在單行道上反向通行，以提高運作靈活性。

1.  允許逆向超車：

> 當逆向超車功能啟用後，車輛可以在單行道上反向通行。
>
> 這項功能通常用於緊急情況或特殊路徑規劃。

2.  路徑距離懲罰：

> 當路徑為逆向時，系統會在計算路徑距離時額外加上很大的懲罰距離。
>
> 這樣的設計是為了避免車輛頻繁選擇逆向路徑，確保逆向超車僅在必要時使用。

#### 5.1.1.9 路名設定 (Road)：

![](media/image60.png)　![](media/image359.png)

　　在路徑屬性中，使用者可以為每個路段設定路名。這項功能幫助使用者更好地識別和管理不同路段，並在路徑規劃中應用特定的優先級策略。

1.  路名設定：

在路徑屬性中，為每個路段設定自定義路名。

預設路名為「main」。

2.  啟用路名優先級策略：

路名設定完後，需要在「齒輪設定」中的「Traffic Control」下，勾選「Enable Straight Road First」選項，才能使路名設定生效。

啟用後，系統會優先選擇路名為「main」的路段進行路徑規劃。

3.  路徑計算優先級：

計算路徑時，系統會以同路名的路段優先行走。

若途中跑到另一條路上，則會視為轉彎，並加上一個懲罰的距離。

![](media/image13.png)

　　 ![](media/image216.png)

　　如圖所示，欲從黃點走到藍點。若路名分為橘路與綠路，則：

> 1 號路徑：換過一次路，相當於轉一次彎。
>
> 2 號路徑：換過兩次路，相當於轉兩次彎。

　　即使1號路徑與2號路徑的長度相同，但因2號路徑轉兩次彎，會獲得更多的懲罰距離，因此系統會選擇1號路徑。

![](media/image308.png)

#### 

### 5.1.2 交管設施（Traffic Control Facilities）：

#### 5.1.2.1 路口點（Junction）：

　　在多路線匯集的點設置 Junction，可以形成一個路口。路口周邊的點即為交管點，用於管理車輛在路口的通行權限。這項功能模擬了人類在十字路口的行為，車輛在接近路口時會先確認是否能取得接下來的路權，若無法取得則會在交管點停下來等待，確保路口通行的安全與順暢。

![](media/image239.png)

※ 圖解：行進時，因綠點為路口點，故紅車會先到紅點處等待，若沒車則繼續通行。

![](media/image407.png) 　![](media/image94.png)

　　當車輛接近路口時，會先取得交管點的路權。當車輛行經路口附近時，會確認是否能取得接下來的路權。若無法取得路權，車輛會在交管點停下來等待，直到取得路權後再繼續前行。

　　若多輛車在路口卡住時，系統會根據車輛的優先級進行處理。優先級較小的車輛會被移動到空巷（如交管點），待塞車疏通後再回到原路徑上。若車輛優先級相同，則系統會隨機選擇一台車進行處理。

![](media/image13.png)

　　 ![](media/image327.png)

　　如圖所示：

> 綠車：優先級較小的車輛，需要往右走。
>
> 橘車：優先級較大的車輛，需要往左走。
>
> 交管點：路口周邊的空巷，用於暫時停放低優先度車輛。

　　當綠車和橘車在路口卡住時，系統會將綠車移動到下面沒有車的交管點，待橘車通過後，綠車再回到原本的路徑，繼續執行其任務。

![](media/image308.png)

　　當設定為Junction的站點與相鄰的站點屬於同一個Group時，系統會將這些站點視為一個大型的路口。這項功能適用於複雜的場地布局，允許系統在多路線匯集的區域進行更靈活的路權管理，確保車輛能夠安全且順暢地通行。

![](media/image13.png)

　　 ![](media/image111.png)

　　如圖所示：

> 黃色點：屬於同一個Group的站點，形成大型路口。
>
> 紅色點：往外延伸的交管點，用於管理車輛的通行權限。

　　當其中一個黃色點被設定為Junction時，所有黃色點會被視為大型的路口。往外延伸的紅色點則是交管點，用於管理車輛的通行權限。車輛在接近大型路口時，會先取得交管點的路權，確認是否能取得接下來的路權，若無法取得則會在交管點停下來等待。

![](media/image308.png)

　　自走車在繞路時會先移動到路口點前的交管點上，可透過將路口點群組（Group）的方式把路口擴大為路口區，劃出更大的範圍讓更多的自走車進行會車，或針對更為複雜的交叉路口使用。

**※ 注意：路口區應為淨空區。**

　　**不應**設置工作站點。

　　**不應**將路口區上的節點跟工作站點設成同一群組。

　　**不應**將路口區的節點與其他路口區的節點設成同一群組。

　　設定完成形成一個交管區域，這個交管區域會成為自走車的淨空區，讓自走車方便調度使用，詳見下圖。

![](media/image121.png)

　　把複數路口點，也就是綠色點 Group 起來，綠色區域是被設為 Group 範圍的淨空區，自走車會在淨空區前的站點，即紅點的位置停下。停下後自走車會判斷誰離淨空區越近，誰就先進入淨空區到橘色的點，誰離淨空區的位置越近，誰就先停靠過去，較遠的自走車就會通行，請見下圖。

![](media/image324.png)

　　從圖中可看見結果，因為藍車先到臨停位置後，紅車發現藍車已經讓開了，就直接通行，前往預定的目的地。

　　另一個方式是劃分一個區域，請見下圖。

![](media/image206.png)

#### 5.1.2.2 交管點（Traffic Point）：

　　與路口點相鄰的節點都是交管點，ACS 系統會自動設置。

#### 5.1.2.3 待命點（Standby Station）：

![](media/image245.png)

　　在自走車設定頁面中，使用者可以設定待命點。待命點是自走車在閒置時會前往停車的位置，系統會自動選擇最近且可到達的待命點，以優化車輛的調度和空間利用。

#### 5.1.2.4 臨停點 (Temporary Park Only)：

![](media/image388.png)

　　在站點屬性中，使用者可以將特定站點設置為臨停點。臨停點是為了應對緊急情況或需要快速調度車輛時，提供額外的停車選項。當需要趕車時，除了待命點外，車輛也可以被趕至臨停點，以提升調度靈活性。

#### 5.1.2.5 尋找替代道路功能 (Find Way Time)：

![](media/image77.png)

　　尋找替代道路功能用於在設定的時間內，若車輛無法沿原路徑通行，系統會自動嘗試尋找替代道路繞路。

#### 5.1.2.6 取得路權超時功能 (GetRightTimeout)：

![](media/image288.png)

　　取得路權超時功能用於在設定的時間內，若車輛無法取得所需的路權，系統會自動跳出異常回報，提示「取得路權超時」。

#### 5.1.2.7 手臂動作中鎖路權(RobotRouteLock)：

![](media/image304.png)

　　手臂動作中鎖路權功能用於在手臂進行動作時，擴大警戒範圍並鎖定附近的站點路權，避免其他車輛進入該區域。

### 5.1.3 塞車解決方法（Traffic Jam Solutions）：

#### 5.1.3.1 趕車（Vehicle Relocation）：

　　趕車功能用於在行經途中發現閒置車輛時，自動將該車輛趕至最近可抵達的待命點。這項功能可以有效管理閒置車輛，避免車輛佔用工作區域或造成路徑堵塞，提升整體運作效率。

　　如果在繞路的路線上，有其他車輛是停車待命（Unassigned）的狀態，則該車會被要求移動到最近、可繞路過去，且不是目的地的停車點上。

![](media/image13.png)

![](media/image282.png)

　　如圖所示：

> 藍點：待命點。
>
> 綠車：需要前往橘車的工作點。
>
> 橘車：閒置狀態（Unassigned）。

　　當綠車需要前往橘車的工作點時，若橘車為閒置狀態，系統會將其趕至最近的可抵達待命點。由於右方的待命點被黃車擋住，因此橘車會被趕至下方的待命點。

![](media/image308.png)

#### 

#### 

#### 

#### 

#### 

####  

#### 5.1.3.2 強制讓道功能 (Force Yielding)：

　　強制讓道功能用於在行經途中遇到低優先度的車輛正在工作時，系統會等待該車輛完成當前工作後，將其趕至附近的停車點讓道。這項功能確保高優先度車輛能夠順利通行，避免因低優先度車輛阻礙而延誤任務。

![](media/image13.png)

![](media/image70.png)

　　如圖所示：

> 藍點：待命點。
>
> 綠車：高優先度車輛。
>
> 橘車：低優先度車輛。
>
> 黃色工作點：綠車需要前往的工作點。

　　當綠車需要前往黃色的工作點時，若橘車正在執行交換貨任務，系統會等待橘車完成該任務。完成後，橘車會被趕至藍色的待命點讓道，綠車則可以順利通行。橘車到達待命點後，會繼續執行剩餘的任務。

![](media/image308.png)

#### 5.1.3.3 重繞路（Re-Detour）：

　　若到路口或目的地的繞路失敗，會等待數秒（Find Way Time），嘗試重新規劃路線再試一次，此時路線規劃會將條件放寬，允許選擇較遠的路線（\< Lowest Cost + Max Find Way Cost）。

#### 5.1.3.4 路口避車（Intersection Avoidance）：

　　當自走車發現路口塞車時，自走車會試著選擇其他非對方自走車路經的交管點上，執行一次繞路。

#### 5.1.3.5 調車（Vehicle Dispatch）：

![](media/image154.png)

　　調車是在遇到雙方會車、或路口塞車無法會車，自走車在繞路產生逾時警示（Timeout Alarm）的情況時，ACS 系統會介入，將該警示解除，保留該輛自走車當下的工作任務，對該輛自走車執行趕車的命令（詳見前文的趕車說明），之後再恢復該輛自走車的工作任務。

#### 5.1.3.5 指定避車點（Designated Avoidance Point）：

![](media/image117.png)

　　避車點（橘色站點）的功用為當該路段路權無法完全取得，但可以取得的路徑中有指定的避車點，則會先行移動到避車點等待，減少未來取得路權後的走行距離。

　　避車點目前有保護措施必須在相鄰的站點避車，避免為了避車而特地繞路進而產生延遲。

#### 5.1.3.6 狹小路段兩車交會（Narrow Lane Vehicle Passing）：

![](media/image171.png)

　　由上方示意圖可見，今天我們在較狹窄的通道進行會車時，發現沒有可以迴避的點位時，可依據現場數據設定成上圖的路線，並做以下設定：

1.  於兩車交會處，也就是綠色點位，設定成 Junction 點。

![](media/image183.png)

2.  設定繞車路線 AltPointID，指向要繞至的點位。

> ![](media/image294.png)

3.  如示意圖，綠色點位處於交集位置，需要設定兩個 Group。

4.  如示意圖，紅色路段請將速度設定降至 50% 以確保安全通行。

![](media/image187.png)　　![](media/image312.png)

5.  實際運行狀況

![](media/image103.png)**　　**![](media/image423.png)

![](media/image420.png)**　　**![](media/image143.png)

## 5.2 搬運任務併車邏輯（Task Merging Logic）

### 5.2.1 情境定義（Scenario Definition）：

　　首先，前面各頁面說明若有看過，可以知道 『TSC 設定』 與 『區域管理』 中都有相關項目，可以至 『批次任務設定（Batch Task Settings）』 觀看詳細說明。

![](media/image126.png)

　　『批次任務設定（Batch Run）』 可以設定搬運任務的任務數量上限。

　　『任務集結逾時（Collect Timeout）』，它所設定的時間表示發送批次命令前的任務集結等待時間。

　　也就是說，基本設定 『Batch Size』 設定為 『6』、『Collect Timeout』 設定為 『15』 的時候，我們每一個任務可以擁有十五秒的任務集結等待時間，等到收集完最多六個任務，或是超過十五秒都沒有新任務進來，就把這個批次命令發送給自走車。

### 5.2.2 範例（Examples）：

　　我們現在透過範例進一步說明這裡的任務合併派送邏輯。

#### 5.2.2.1 併車邏輯範例一、合併交換料任務（Merging Exchange Tasks）：

![](media/image302.png)

　　今天我們有這些可能沒有經過篩選的任務，假設任務在手動輸入或匯入時不照順序的加到搬運任務的 『等待佇列（Waiting Queue）』 中。

　　這時我們的系統就會依照上面的基本設定開始進行整理，在每次新任務進來的時候系統都會重新排序，還記得基本設定的條件嗎？

『Batch Size』 為 『6』 個

『Collect Timeout』 為 『15』 秒

![](media/image34.png)

　　所以任務數量達到六個，或是任務集結等待的時間超過十五秒還沒有新任務時，它就會整理集結成一個批次命令，發送給自走車，身為第七個的 『D機上料』 就會留到下次的批次命令。

　　透過圖片，我們能夠發現它的任務整理邏輯，不論先後，系統會計算出包含這些任務的最短、最快、最佳路徑送到交給自走車，出現在 『執行佇列（Execution Queue）』。

　　

　　於是自走車就會在這一批的運送命令中，開始從最近的 Ａ機台 開始下料，然後上料；接下來到 Ｂ機台 進行下料，再來上料；最後到 Ｃ機台 進行下料，再來上料。

　　此時，自走車便完成這一批次命令的運送，回到它的待命地點。

#### 5.2.2.2 併車邏輯範例二、合併上下料任務（Merging Loading and Unloading Tasks）：

![](media/image269.png)

　　想要執行的任務都屬於在個別機台只進行一次動作的情況下會怎樣呢？

　　

　　這時我們需要注意一件特別重要的事情，自走車上依型號不同，會有不同數量的槽位。例如範例中的設定是擁有四格儲位的 Gyrobot Type A，它能夠同時擺放四個載具進行運送。

![](media/image380.png)

　　所以在排序以後，儘管我們有設定單次能夠集結的任務數量上限六個，但因為攜帶數量的限制，自走車也只能接到四個任務進行批次處理。

　　尋找最短路徑把 Ａ、Ｂ、Ｃ、Ｄ 四個站台的任務完成。

#### 5.2.2.3 併車邏輯範例三、合併交換料與上下料任務（ Merging Exchange and Loading/Unloading Tasks）：

![](media/image169.png)

　　最後我們來看最貼近實際運作的狀況，兩者混合在一起的複合動作，其實在前面可以大致了解當這些情況同時出現會是什麼樣子了，我們來看相同情境下的複合動作會如何執行。

於是我們可以看到，它會在排序後將相同機台的任務合併為一組，接著依照路徑的最短距離進行排序。

![](media/image95.png)

　　

　　而在 『合併交換料與上下料任務』 中還有一個可能，假如等待佇列中有能夠組合成兩組交換料的任務，它會按順序排列。

　　

![](media/image401.png)

　　因為交換料與上下料需要一個空位進行擺放，為維持安全運作，批次命令包含的載具數量基本為三個，即自走車上儲位減去一。

## 5.3 群組設計原則 ( Group Define )

### 5.3.1 群組設計的定義（Group Design Definition）：

　　Group 功能設計的意義是，當兩站點過於靠近，不允許兩輛自走車同時在這個區域。

### 5.3.2 自走車規格（AGV Specifications）：

自走車尺寸（AGV Dimensions）：長 120 公分 x 寬 72 公分。

安全範圍（Safety Range）：

前進時：

> 距離前方目標 75 公分 時會進行減速，距離目標 60 公分 時停止。
>
> 側邊距離目標 35 公分 時停止。

橫移時：

> 距離前方目標 30 公分 時會進行減速，距離目標 25 公分 時停止。
>
> 側邊距離目標 50 公分 時減速，距離目標 35 公分 時停止。

### 5.3.3 群組設計（Group Design）：

　　根據上方的自走車規格可以得知，對於一個站點來說，從地圖編輯的平面來看，上下長度為 180 公分 的站點必須被 Group 保護，左右長度為 110 公分 的站點必須被 Group 保護。（自車半截車身 + 停止區域 + 來車半截車身）

　　為了簡化距離的概念，方便使用者定義，我們有以下幾個設定指導原則。

#### 5.3.3.1 基本規則第一點（Basic Rule 1）：

![](media/image33.png)

　　上圖可見，若在規劃路線時需要一個旋轉點，可在地圖編輯時將兩個站點設定為行走方向不同的站點後，將其重疊，再設定成同一個 Group。

#### 5.3.3.2 基本規則第二點（Basic Rule 2）：

![](media/image229.png)

　　在同一個機台有多個 Loadport 的情況下，在理論上同時間會交付給同一台自走車執行任務，因此將其設定為同一個 Group。

#### 5.3.3.3 基本規則第三點（Basic Rule 3）：

![](media/image246.png)

　　而針對相鄰機台的 Loadport，若彼此間的距離小於設計原則的距離，則需額外加上一個 Group 予以保護，請見上圖。

#### 5.3.3.4 基本規則第四點（Basic Rule 4）：

![](media/image338.png)

　　位於路口處，若附近的站點彼此間的距離小於設計原則，則全部設為同一個 Group。

#### 5.3.3.5 特殊情境 1 - 路口點 (\*註1)（Special Scenario 1 - Junction）：

![](media/image89.png)

　　若在路口點旁塞車會啟動路口避車機制（\*註2），因此需檢查在路口點旁的兩台自走車會不會互相卡住。

註1： 關於 JUNCTION 點，即路口點的說明請見 5.1.2.1 路口點（Junction）。

註2： 關於路口避車的說明請見 5.1.3.3 路口避車（Intersection Avoidance）。

![](media/image283.png)

　　如圖 2，按照設計原則，E20001 的 Group 需涵蓋到 J201，如圖中的綠色框所示。

　　然而按此案例設定，若兩台自走車分別停在路口外的 E20001 與 P2018 上，位於 E20001 的自走車要往上，位於 P2018 的自走車要往下，這樣會造成無處可避的情形。

　　若將案例中路口點的 Group 設定往 E20001 延伸，將其包含在內，見圖 3。那麼位於 E20001 的自走車會因為範圍擴大，退到 E20002，便可以讓 P2018 的自走車往下通行。

#### 5.3.3.6 特殊情境 2 - 雙線道（Special Scenario 2 - Dual Lane）：

![](media/image12.png)

　　Group 必需是相連在一起的站點群集，因此需避免規劃出相同 Group 但站點不相鄰的路徑。如圖 1 的 Group 1 與 Group 2，都是相連的站點。

![](media/image19.png)

　　此時我們重點放在圖 2 的 Group 上，紅色框為 Group 1，綠色框為 Group 2。若自走車規劃出的路徑如橘色箭頭，我們可以發現，路徑 E20001 ➡ P2018 ➡ P2046 會經過 Group1 ➡ Group2 ➡ Group1。這樣不連續的情形會造成自走車在經過 E20001 之後，Group1 的路權會被提早釋放，導致其他自走車可以進入 Group1 的站點。

![](media/image54.png)

　　因此，需同圖 3，將 Group 2 的範圍納入 Group1，才不會造成提早釋出路權的情形。

## 5.4 Log 解讀 ( Log Interpretation )

### 5.4.1 收到移動路徑指令 (Receiving Movement Path Command)：

　　在系統運行過程中，LOG 記錄了車輛移動路徑的相關訊息。這些訊息可以幫助使用者了解車輛的移動狀態、路徑規劃過程以及路權處理的進展。以下是 LOG 中常見的訊息及其解讀。

#### 5.4.1.1 Get move_control...：

#### ![](media/image90.png)

　　這表示 TSC 系統管理車輛的模組，已經成功接收到了一項新的移動任務或指令。

#### 5.4.1.2 path: deque(\[\[...\], \[...\], ...\])：

#### ![](media/image287.png)

　　通常在系統接收到移動指令後，會開始規劃或更新車輛的詳細行走路徑。把新的路段指令拆解，然後加到車輛目前的路徑序列中。完成這些計算後，就可能看到這個訊息。

#### 5.4.1.3 get_right...：

#### ![](media/image392.png)

　　當看到這個訊息時，表示系統已經進入到處理「路權」的階段。

### 5.4.2 下達移動命令 (Issuing Movement Command)：

#### 5.4.2.1 Get Lock：

![](media/image86.png)

　　這條訊息代表系統已取得 threading 的 lock (鎖)。這個鎖的作用是避免多輛車同時計算路徑時產生衝突，確保路徑計算的同步性。

#### 5.4.2.2 路權確認：

　　在取得鎖之後，系統會進行路權的確認，確保車輛能夠順利取得所需的路權。如果路權確認沒有問題，系統會對自走車下達移動命令。

#### 5.4.2.3 move_cmd...：

![](media/image193.png)

　　這條訊息代表系統已經下達移動命令。訊息後面會跟隨一串站點的詳細資訊，包括站點名、X、Y、Z、W座標、Keep/go屬性、是否進退站以及速度。

### 5.4.3 過站不停命令 (Pass-Through Command)：

　　過站不停命令功能用於在車輛原本需要在某個交管點停下的情況下，臨時改變指令，讓車輛繼續前進而不停靠該站點。這項功能適用於需要快速調整路徑或避免不必要的停頓的場景。

![](media/image357.png)

　　若原先會在交管點停下，但之後需要繼續前進，則為標示為C。

　　當有一個新的Go點被下達後，會下 change cmd 給自走車，通知自走車將原先交管點的 Go 點忽視。

### 5.4.4 路權管理 (Right-of-Way Management)：

![](media/image309.png)　![](media/image172.png)

#### 5.4.4.1 路權釋放的基礎：車輛位置回報 (Vehicle Position Reporting)：

　　當自走車開始依照指令移動時，它會持續向中央管理系統回報自身的即時位置。

　　系統會根據這些回報的位置資訊，判斷自走車已經安全通過了哪些路段。

　　一旦確認某路段已被自走車通過且不再需要，系統就會「釋放」該路段的路權，使其能被分配給其他等待的自走車。這個過程對於維持交通流暢至關重要。

#### 5.4.4.2 路權釋放模式 (Right-of-Way Release Modes)：

　　系統通常會根據預設的策略來決定釋放路權的確切時機點，常見的模式有以下幾種：

1.  模式一：整段路徑完成後釋放：

> 自走車必須走完分配給它的一整段完整路徑後，系統才將這整段路徑所佔用的路權一次性全部釋放。

2.  模式二：到站後釋放：

> 當自走車成功抵達指定的停靠站點後，系統會立即釋放它從上一點到目前抵達站點之間所行駛過路段的路權。

3.  模式三：離站後釋放：

> 當自走車完成在站點的任務（例如裝卸貨）並開始離開該站點，朝向下一個目標移動時，系統才會釋放剛剛離開的那個站點本身以及到達該站點前所經過路段的路權。這種模式可以確保站點區域在車輛完全駛離後才變為可用。

#### 5.4.4.3 日誌中的路權資訊解讀 (Interpreting RoW Information in Logs)：

　　在系統的運行日誌 (Log) 中，您可能會看到與路權管理相關的記錄，其格式可能類似：「站點名稱, 數字, \[路徑列表\]」。這些欄位通常包含以下資訊：

1.  站點名稱 (Station Name)：

> 代表與目前路權狀態相關的參考點。可能是自走車目前最接近的站點、下一個目標站點，或是路權計算的基準點。

2.  數字 (Index / Counter)：

> 這通常是一個索引值或計數器，用來表示自走車在當前持有的路權路徑上的進展。例如，它可能指示自走車已經通過到路權列表中的第幾個點，或者還有多少點的路權尚未釋放。

3.  \[路徑列表\] (List of Path Points/Segments)：

> 這是一個列表 (List)，其中包含了該自走車目前仍然持有路權的一系列路徑點或路段。隨著自走車前進並根據上述模式釋放路權，這個列表的內容會動態更新（例如，已通過的點會從列表中移除）。

### 5.4.5 路權管理 (Right-of-Way Management)：

　　自走車抵達目的地和隨後的路權釋放是任務流程中的重要環節。

#### 5.4.5.1 抵達站點訊息 (Arrival Messages)︰

![](media/image322.png)

1.  Arrival point 訊息：

> 　　當自走車實際抵達其任務指令中設定的任何一個目標點（Go 點）時，系統通常會發出或記錄一條 Arrival point 訊息，確認已到達該指定位置。

2.  End Arrival 訊息：

> 　　如果自走車抵達的這個點是整個任務流程的「最終站點」，系統會發出一個 End Arrival 訊息。這表示車輛已完成主要的行駛任務，抵達最終目的地。

#### 5.4.5.2 路權釋放的判斷與日誌記錄 (RoW Release Logic and Logging)：

![](media/image364.png)

1.  釋放時機：

> 　　系統會根據先前設定的模式（例如「到站後釋放」或「離站後釋放」）來嘗試釋放不再需要的路權。

2.  群組釋放邏輯：

> 　　在釋放過程中，系統會檢查目前自走車還佔用著哪些路權點位。這些點位可能被分成不同的「群組」(group)，代表邏輯上連續或相關的路段。當系統成功釋放了某個群組內的所有點位，使得剩餘佔用的點位都屬於其他不同群組時，則會印出 Release: group。

3.  Release: \[group_name\] 訊息：

> 　　這個記錄通常會以類似 Release: \[group_name\] 的形式出現，其中 \[group_name\] 是剛剛被完整釋放掉的那個路權群組的名稱或識別碼。這條訊息幫助追蹤哪些路段的路權已經被成功歸還給系統。

4.  終點站標記：

> 　　如果被釋放的這個路權群組 (\[group_name\]) 恰好包含了任務的「終點站」，那麼為了在日誌中更容易區分，系統可能會在這條 Release 訊息後面額外加上一個星號（\*），顯示為 Release: \[group_name\]\*。這算是一個特殊的標記，提醒開發者或維護人員，這是包含最終目的地的路權釋放事件。

