---
title: 齊宏洋 TSC 技術問答與異常處理
description: 涵蓋路段佔用、位置管理、Robot Area、Deadlock、報警分析及動態選路等 TSC 核心技術
tags: [TSC, Deadlock, Robot Area, Alarm, FAQ, RAG]
---

## 路段占用阻塞 (global_occupied_station)

### Q1：車輛 A 停止不動，log 顯示 'Blocked at [route, group] by 車輛B'，是什麼原因？
**A：** 這是標準的「路段佔用阻塞」。車輛 A 前方路段的 group 已被車輛 B 登記在 global_occupied_station 中。系統同步發出 VehicleTrafficBlocking 事件，車輛 A 進入等待取路權狀態。此時屬於正常的交管保護機制，不需要立即介入，應先觀察車輛 B 是否持續移動並釋放路段。

### Q2：車輛 B 已經離開某路段，但車輛 A 仍顯示被 B 阻塞，可能原因是什麼？
**A：** 可能是車輛 B 未正確執行 clean_right() 或 clean_path()，導致 global_occupied_station 中的 group 沒有被清空。排查方向：（1）確認車輛 B 的 last_point 是否已更新至新位置；（2）檢查 occupied_route 是否已清除；（3）查看是否有例外（Exception）導致 release 流程中斷。

### Q3：什麼情況下 global_occupied_station 的 group 會被清空（Release）？
**A：** 有兩個時機：（1）車輛通過路段時，在 clean_path() 中逐步釋放已通過的節點；（2）任務結束或異常中止時，在 clean_right() 中全部清空。若車輛異常停止或 thread 被強制結束，clean_right() 必須被呼叫，否則 group 會殘留，造成後續車輛永久阻塞。

### Q4：如何從 log 快速判斷阻塞是由 occupied_station 還是 vehicles_location 引起的？
**A：** 從 log 前綴可以判斷：「Blocked at」（無星號）代表 global_occupied_station 阻塞；「*Blocked at」（一個星號）代表 global_vehicles_location 阻塞；「**Blocked at」（兩個星號）代表 global_vehicles_robot_area 阻塞。三種阻塞的處理方式不同，需先確認前綴再進行分析。

---

## 車輛當前位置 (global_vehicles_location)

### Q5：什麼是 block_by_still_car？它與一般阻塞有什麼不同？
**A：** block_by_still_car=True 代表前方阻塞的車輛是靜止的（由 global_vehicles_location 判斷），而非佔用了路段路權。此時系統不只等待，還會發出 global_moveout_request 要求對方移動讓路，並在等待一段時間後嘗試繞路（Find Way）。一般的 occupied_station 阻塞則不會觸發 moveout_request 和繞路機制。

### Q6：global_vehicles_location 和 global_occupied_station 有何本質差異？
**A：** global_vehicles_location 記錄車輛「目前實際所在位置」的 group，在 update_location() 中根據真實座標更新；global_occupied_station 記錄車輛「已預先鎖定的路段路權」，在取得路線右（get_route）時提前設定。前者代表車在哪裡，後者代表車打算走哪裡。兩者都可能阻塞其他車輛，但觸發的處理流程不同。

### Q7：車輛位置（VehiclePose）和 last_point 不一致時，會造成什麼問題？
**A：** 若車輛實際座標已移動但 last_point 未更新（例如定位訊號丟失），global_vehicles_location 會殘留在舊位置的 group，導致其他車輛誤以為舊路段仍被佔用而停止等待。這種情況可從 log 看到 'update_location' 未被觸發。

### Q8：moveout_request 發出後，如果對方車輛沒有回應，系統會怎麼處理？
**A：** 系統會持續等待並嘗試透過 Find Way 機制計算繞路。若繞路代價過高或找不到替代路徑，會繼續等待直到 get_right_timeout（180秒）超時，最終觸發 alarm 900001，強制清除路由並停止該車輛任務。

---

## 車輛作業中占用 (global_vehicles_robot_area)

### Q9：什麼是 RobotRouteLock？什麼時候會生效？
**A：** RobotRouteLock 是 PoseTable 節點的一個屬性，設定後代表該節點周圍有機械手臂作業範圍保護區域。當車輛抵達設有 RobotRouteLock 的點時，系統會在 update_location() 中將對應的 group 登記到 global_vehicles_robot_area，防止其他車輛進入相同區域，避免與機械手臂發生碰撞。

### Q10：robot area 什麼時候會被釋放？如果沒有被釋放怎麼辦？
**A：** robot area 在車輛離開該點（抵達下一個位置）並執行 update_location() 時，會透過 memory_robot_area 比對清除舊的 group。若車輛任務異常中止，會在 clean_right() 或 thread 結束的 run() 尾段執行清除。若發現 robot area 殘留，可手動觸發重新定位或重置車輛狀態，強制執行 clean_right。

### Q11：log 顯示 '**Blocked at' 時，應該如何排查？
**A：** 這代表被 global_vehicles_robot_area 阻塞。排查步驟：（1）確認阻塞者的 group 屬於哪個節點的 RobotRouteLock；（2）確認阻塞者車輛目前是否仍在執行機械手臂動作（如取放貨）；（3）若阻塞者已完成作業但未離開，可能是任務卡住，需確認其 AgvState 和 action_in_run；（4）若阻塞者已離開但 robot_area 未清，需手動重置。

---

## Deadlock 判斷與排解

### Q12：什麼情況下系統會判定發生死鎖？
**A：** 系統透過追蹤 global_moveout_request 鏈來偵測死鎖。若車輛 A 等待 B 讓路（moveout_request[A]=B），B 又等待 A 讓路（moveout_request[B]=A），形成循環（check_id 追蹤回到 self.id），且雙方車輛的 global_vehicles_priority 相同，系統判定為死鎖（check=True）。

### Q13：死鎖判定後，系統會自動解除嗎？需要人工介入嗎？
**A：** 系統會嘗試自動解除。死鎖確認後若持續超過 10 秒沒有進展，會將 get_route_timeout 設為 True，強制清除該車輛的路由計畫（global_plan_route），觸發 alarm 900001 並停止任務。通常不需要立即人工介入，但若同一路線反覆死鎖，代表路網設計有問題（如雙向單行道交叉），需要修改地圖或調整派車邏輯。

### Q14：如何從 log 確認是死鎖還是單純的等待超時？
**A：** 死鎖的特徵是：兩台車的 moveout_request 互相指向對方，且兩台車的 log 都出現 'Find new route' 且代價過高無法繞路。單純等待超時只有一台車的 log 顯示持續 'Blocked at'，另一台車仍在正常移動。可以同時查看兩台車的 global_plan_route 和 moveout_request 來比對。

### Q15：優先級（global_vehicles_priority）如何影響死鎖解除？
**A：** 只有當循環等待的車輛優先級相同時，才會判定為死鎖並強制超時。若其中一台車優先級較高，系統期望低優先級車輛讓路，不觸發強制超時，而是持續等待對方移動。因此，若想降低死鎖機率，可以為不同任務類型的車輛設定不同優先級，讓系統能自然解除等待。

---

## 逾時報警 (Alarm 900001)

### Q16：Alarm 900001 代表什麼？觸發條件是什麼？
**A：** Alarm 900001 代表「取路權逾時」。當車輛等待取得下一段路權的時間超過 get_right_timeout（預設 180 秒，加上 0~20 秒隨機值）時觸發。觸發後系統強制將車輛狀態設為 Idle、清除 current_route，車輛停在原地等待人工重新派車。

### Q17：為什麼 get_right_timeout 設計有 0~20 秒的隨機值？
**A：** 隨機值是為了避免多台車同時發生超時，造成系統在同一時間集中處理大量 alarm 和路由重建。加入隨機值後，各車的超時時間會錯開，降低系統負載，也減少多台車同時搶奪路權的競爭情況。

### Q18：900001 觸發後，車輛路由被清除，後續應如何恢復任務？
**A：** 車輛狀態變為 Idle 後，上層系統（TSC）應重新下達派車指令。若阻塞根因未解除（如其他車輛仍擋在路上），新任務會再次觸發 900001。建議先確認並解除阻塞原因後，再重新下達任務，避免反覆觸發 alarm。

### Q19：如何預防 900001 頻繁觸發？
**A：** （1）確保 global_occupied_station 和 global_vehicles_location 正確即時更新，避免路段殘留；（2）啟用 enable_find_way=True，讓車輛在阻塞時能自動繞路；（3）合理設計路網，避免瓶頸節點（如單一出入口）；（4）對高優先任務設定較高的 global_vehicles_priority；（5）監控各車 moveout_request 鏈，及早發現死鎖跡跡象。

---

## 動態繞路 (Find Way)

### Q20：什麼條件下會觸發 Find Way 繞路？
**A：** 同時滿足以下條件才觸發：（1）block_by_still_car=True（被靜止車輛阻塞）；（2）enable_find_way=True（繞路功能已開啟）；（3）等待時間超過 find_way_time * (find_way_cnt+1) 秒（每次嘗試間隔遞增）；（4）is_junction_avoid 不等於 1（非路口迴避狀態）。或者 force_find_way=True 時直接強制觸發。

### Q21：Find Way 找到新路徑後，為什麼有時候不採用？
**A：** 系統會比較新路徑代價（new_cost）與原路徑代價（origin_cost）的差值，若差值超過 max_find_way_cost（預設 60000），則放棄新路徑繼續等待。這是為了避免車輛繞行過遠、浪費時間。若路網壅塞嚴重導致所有替代路徑代價都過高，系統會持續等待直到超時。

### Q22：find_way_cnt 的作用是什麼？它如何影響繞路行為？
**A：** find_way_cnt 是繞路嘗試次數計數器。每次觸發 Find Way 後遞增，使得下次觸發的等待門檻變高（find_way_time * (find_way_cnt+1)）。這樣設計是為了避免短時間內頻繁重新計算路徑，給前方車輛更多時間自行移動。當車輛成功開始移動（is_moving=True）後，find_way_cnt 會重置為 0。

### Q23：Find Way 繞路使用什麼演算法？block_nodes 是如何決定的？
**A：** 系統呼叫 Route.h.get_a_route() 進行路徑計算，演算法由 global_variables.RouteAlgo 決定（通常為 A*）。block_nodes 包含：（1）所有其他車輛目前 location_index 對應 group 的節點；（2）global_disable_nodes（系統禁用節點）；（3）global_point_Blacklist（該車的黑名單節點）；（4）global_disable_edges（禁用邊）。

---

## 宏動作與流程 (Macro)

### Q24：車輛卡在某個節點無法前進，log 沒有 'Blocked at' 訊息，可能是什麼原因？
**A：** 很可能是 PreProcess 或 PostProcess 的設備動作失敗導致路由中止。程式中設備動作（如 gate_open、grd_open、elevator_open 等）若回傳 False，會直接 return 中斷當前路由執行，但不產生 Blocked at 的 log。應檢查該節點是否設有 PreProcess/PostProcess 屬性，並查看對應設備的通訊 log 是否有錯誤。

### Q25：電梯相關動作（go_elevator、go_floor、change_floor）的執行順序是什麼？哪個步驟最容易失敗？
**A：** 完整流程為：call_elevator（召梯）→ elevator_open（等梯門開）→ wait（等待）→ moving_in_elevator（車輛進梯）→ move_in_elevator_complete → elevator_close（關梯門）→ elevator_move（電梯移動）→ change_route（切換樓層地圖）→ elevator_open（到達開門）→ moving_out_elevator（車輛出梯）→ move_out_elevator_complete → elevator_close（關門）。最容易失敗的是 elevator_open 等待逾時（電梯門未開）和 change_route（樓層地圖切換失敗）。

---

## 位置重疊報警 (Alarm 900000)

### Q26：Alarm 900000 代表什麼？觸發條件是什麼？
**A：** Alarm 900000 代表「車輛位置重疊（Overlap）」。當車輛完成移動並更新位置時，發現目標位置的 group 已被另一台車登記在 global_occupied_station 或 global_vehicles_location 或 global_vehicles_robot_area 中，系統判定為重疊，強制將車輛狀態重設為 Idle 並觸發此 alarm。

### Q27：發生 Overlap 的常見根因有哪些？
**A：** 主要有三類：（1）地圖 group 設定錯誤：兩個物理上可以共存的節點（如並排位置）被設定為同一 group，導致系統誤判重疊；（2）車輛定位偏差：感測器精度不足，車輛被定位到鄰近節點，與實際在那裡的車輛衝突；（3）cleanup 遺漏：前一輛車離時未正確清除 group，導致下一輛車到達時仍看到舊的佔用記錄。

### Q28：Alarm 900000 觸發後，被錯誤清除的路段資訊如何恢復？
**A：** Alarm 900000 觸發時系統會觸發alarm。若兩台車的 group 確實有衝突，需人工確認兩台車的實際位置後，重新下達任務。若是地圖 group 設定錯誤，需修正 PoseTable 中相關節點的 group 值，讓物理上可共存的節點使用不同 group。

---

## 排查建議

### Q29：操作人員看到多台車在路口互相等待但沒有觸發 alarm，應該觀察哪些指標來判斷是否需要介入？
**A：** 建議觀察以下指標：（1）等待時間：超過 60 秒且沒有任何車輛移動，需開始關注；（2）VehicleBlocking 事件：確認 BlockedBy 和 BlockedByStillCar 的內容，判斷是動態阻塞還是靜止車輛阻塞；（3）global_moveout_request：若多台車互相指向對方，代表可能存在死鎖；（4）Find Way 嘗試次數（find_way_cnt）：若已多次嘗試繞路失敗，代表路網嚴重壅塞，可能需要人工移車。
