#initialize and reset
import time
import system
import traceback
tu_serID = str(system.tag.read('Path/TU/tu_serID').value)
def init_reset():
	system.tag.write('Path/instruction',"")
	system.tag.write('Path/spoolRun',"Single")
	
	
	
#same function for abort and run out. 
#6.22.18 PPC
#only the directive is different between these two. abort vs. run_out

def func2(select):
	#response = system.net.httpGet('http://nordevapp01.corp.int/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=abort;mach_no=601;oper_id=ITS;layout_id=JHE;layout_passwd=JHE123;reason=MT;')
	#system.net.httpGet('http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=abort;mach_no=601;oper_id=167;layout_id=JIH;reason=MT;layout_passwd=JIHAB3')
	import time
	import system
	reason = ''
	

	try:
		svc='rewind_aux/rewind_aux.svc/process?inString='
	
		if select == 'abort':
			directive = 'abort'
		else:
			directive = 'run_out'
		print directive
		
		data = 'directive=' + directive
		data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value)
		data+= ';oper_id='+ str(system.tag.read('Path/layout_id').value).upper()
		#JIH I need to preserve the oper id with a new tag
		#data+= ';oper_id='+ 'JIH'
		data+= ';layout_id='+ str(system.tag.read('Path/layout_id').value).upper()
		data+=';layout_passwd=' + str(system.tag.read('Path/layout_pw').value).upper()
		#data+= ';layout_id='+ 'JIH'
		#data+=';layout_passwd=' + 'TASHA7'
		#abort reason parse
		abort_reason = (str(system.tag.read('Path/abort_reason').value))
		

		if abort_reason == '0': 
			reason = 'MT'
		elif abort_reason == '1':
			reason = 'ME'
		elif abort_reason == '2':
			reason = 'BQ'
		elif abort_reason == '3':
			reason = 'BR'
		elif abort_reason == '4':
			reason = 'BS'
		elif abort_reason == '5':
			reason = 'CC'
		elif abort_reason == '6':
			reason = 'LE'
		elif abort_reason == '7':
			reason = 'WP'
		print reason + 'reason'		

		data+=';reason='+ reason
	#	
		
		
		sendstring = (PTS_URL+svc+data)
		print sendstring
		log('SEND: ' + sendstring)
		response = system.net.httpGet(sendstring)
		print response
		log('GOT: ' + response)
		
		
		responsesp = response.split(':')
		response_size = response.count(':')
		print response_size
		
		system.tag.write('Path/bTrue',0) #BOOLS ASSOCIATED WITH THE VISIBILITY OF EACH OF THE ABORT DIALOG BOX. 
		system.tag.write('Path/bTrue2',0)
#		system.tag.write('Path/po_removeID',1)
		#system.tag.write('Path/po_fiberID', '')
		#system.tag.write('Path/po_serID', '')
#		system.tag.write('Path/TU/nextID', '')
#		system.tag.write('Path/TU/CutLenSet_pts', '')
#		system.tag.write('Path/TU/tu_plan_area', '')
#		system.tag.write('Path/po_len_set', '')
#		system.tag.write('Path/po_serID_hidden', '')
#		time.sleep(1)
#		system.tag.write('Path/po_removeID',0)
		
		#if there is not a 0 code. 0 = good, 4 = error
		if responsesp[5] != '0' and response_size > 5:
			
			if responsesp[6] == 'Invalid password or layout id. ' or 'Failed to get layout id.': #'Invalid password or layout id. ':
				system.gui.messageBox(responsesp[6])
				system.tag.write('Path/instruction',responsesp[6])
				system.tag.write('Path/layout_reject', 0)
				
			system.tag.write('Path/instruction',responsesp[6] + responsesp[7])
	
		
		else:
				
				system.tag.write('Path/po_removeID',1)
				system.tag.write('Path/TU/nextID', '')
				system.tag.write('Path/TU/CutLenSet_pts', '')
				system.tag.write('Path/TU/tu_plan_area', '')
				system.tag.write('Path/po_len_set', '')
				system.tag.write('Path/po_serID_hidden', '')
				system.tag.write('Path/TU/tu_plan_area','')
				time.sleep(1)
				system.tag.write('Path/po_removeID',0)
				system.gui.messageBox(responsesp[6])

	except:
		log(traceback.format_exc())
		
#SCRIPT IS RAN WHEN THE OK BUTTON IS PRESSED AFTER LOGGING IN THE ABORT TU SPOOL

		
def tu_abort():

	layout_id = str(system.tag.read('Path/layout_id').value).upper()
	layout_passwd = str(system.tag.read('Path/layout_pw').value).upper()
	
	if layout_id == 'ADMIN' and layout_passwd == 'OFS12345':
		system.tag.write('Path/TU/previous_completed',1)
		system.tag.write('Path/instruction','TU spool aborted')
		shared.main.log('TU spool is aborted or scrapped')
		
	else:
		system.gui.messageBox('invalid username or password')
	system.tag.write('Path/bTrue3',0)
	


def func():
	pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185
	po_length = system.tag.read('Path/po_len_set').value
	current_length = system.tag.read('Path/TU/take_len').value
	diameter = system.tag.read('Path/po_diameter').value
	po_cen = po_length - current_length
	circ = int(pi * diameter)/1000.0

	logPitch = 'PITCH CHANGE DETECTED - ' + str(circ)+':0:'+str(po_cen)+':0:0'
	#ADDED CURRENT_LEGNTH TO THE PITCH (PPC 080118)
	system.tag.write('Path/PITCH',str(circ)+':'+str(current_length)+':'+str(po_cen)+':0:0')
	shared.main.log(logPitch)


def Calibrate(): #check calibration

	svc= 'rewind_aux/rewind_aux.svc/process?inString='
	tu_ten = round(system.tag.read('Path/fWindingTensionMe').value,2)
	pf_ten = round(system.tag.read('Path/Calib/fProofTensionCalibCheckMe').value,2)

	#pf_tension and tu_tension  nominal setpoint values 
	pf_ns = system.tag.read('Path/Calib/fProofTensionCalibMaxNs').value
	tu_ns = system.tag.read('Path/Calib/fTensionCalibMaxNs').value

	#call of inTolerance function
	if shared.main.inTolerance(pf_ns,5.0, pf_ten):
		pf_st = "YES:" #tu status
	else:
		pf_st = "NO:"
	print pf_ten
		
	if shared.main.inTolerance(tu_ns,5.0,tu_ten):
		tu_st = "YES:" #tu status
	else:
		tu_st = "NO:"
	print tu_ten

	mach_no = system.tag.read('Path/mach_no.value')
	oper_id = system.tag.read('Path/oper_id').value.upper()
	data= 'directive=calibrate_mach'	
	data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value) 
	data+= ';oper_id=' + str(system.tag.read('Path/current_oper_id').value) 
	data += ';calibrate_data=POLC:YES:0' + ':' #N/A for nextrom new mach
	data+= ':TULC:' + str(tu_st) + str(tu_ten)  #eg: YES:-55.952:
	data += ':PTLC:'+ str(pf_st) + str(pf_ten)

	try:
		sendstring1 = shared.main.PTS_URL + svc + data #UNCOMMENT AFTER TESTING 
		#sendstring1 = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467:'
		shared.main.log(sendstring1)
		print sendstring1
		response = system.net.httpGet(sendstring1)
		shared.main.log(response)
		print response
		
		responsesp = response.split(':')
		
		system.tag.write('Path/instruction', responsesp[6])
		
	except:
		
		shared.main.log('Calibrate send error has occured')
		print 'error'
		




def testCalibrate():
	import system

	sendstring1 = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467:'
	
	print sendstring1
	response = system.net.httpGet(sendstring1)
	
	print response
	
	responsesp = response.split(':')
	shared.main.log(response)
	system.tag.write('Path/instruction', responsesp[6])#+responsesp[6])

	#http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467:


	#Complete TU 
#triggered by "Complete" button by the PLC 
#Corresponds to TVerifyTakeup Function on NETUTIL.bas 

#COMPLETE TU		
#Example:  http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/completeTU/completeTU.svc/process?inString=mach_no=770;oper_id=117;
#po_id=JRFVY3889A1RVJ;po_serial_id=3800125904;rwr_id=RWR551295121;rwr_serial_id=5206475492;
#plan_length=50550;actual_len=50551;accum_len=50555;tu_color=GR;tu_status=OK;stop_code=STCT;
#mach_speed=1500;spoolRun=Single;I_PO_TEN=66.5:72.7:1.45:69.48;I_TU_TEN=45.4:55.3:1.83:49.78;
#I_PF_TEN=106.1:114.7:1.82:109.75;SPEDGE=30.54:29.77:-0.49:175.56:176.35:0.39:;DEFECT=0:0;MISC=21
import system 
import time 
import traceback
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU
def CompleteTU():
	tu_length = system.tag.read('Path/TU/take_len').value #move the OPC Path/take_length to a local memory tag. Fix the TUpkg not being sent issue. Reset this later. 
	system.tag.write('Path/TU/tu_length',tu_length)
	
	time.sleep(5)
	
	try:
#http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/completeTU/completeTU.svc/process?inString=mach_no=601;oper_id=200;
#po_id=;po_serial_id=;rwr_id=RWR722616469;rwr_serial_id=5220158737;plan_length=26074;actual_len=1380;accum_len=1380;tu_color=BL;tu_status=OK;stop_code=PFBK;mach_speed=0;I_PO_TEN=0.0:0.0:0.0:0.0;I_TU_TEN=0:0:0.0:0.0;I_PF_TEN=0:0:0.0:0.0;SPEDGE=156.15:156.15:0.0:9.92:9.92:0.0:;MISC=21

		svc= 'completeTU/completeTU.svc/process?inString=' #TU Svc 
	
		#postData2= "directive=" + directive2 +';' 
		postdata= 'mach_no=601' 
		postdata+= ';oper_id=' + str(system.tag.read('Path/current_operid').value).upper()
		postdata+= ';po_id=' + str(system.tag.read('Path/po_fiberID').value)
		postdata+= ';po_serial_id=' + str(system.tag.read('Path/po_serID').value) 
			
		postdata+= ';rwr_id=' + str(system.tag.read('Path/TU/tu_fiberID').value)
		
		manual_mode = system.tag.read('Path/manual_mode')
		
		#SPEDGE PARAMETERS ADDED 7/16/18 -  PPC
		
		spedge_tags = ['Path/Spedge/init_begin_outer','Path/Spedge/actual_begin_outer','Path/Spedge/begin_error_outer','Path/Spedge/init_end_inner','Path/Spedge/actual_end_inner','Path/Spedge/end_error_inner']
		lst = (system.tag.readAll(spedge_tags))
		#inner and outer are what is referreced as end and begin (respectively) on the nextrom plc 
		#outer = begin
		#inner = end 
		#str(round(d0,2))
		spedge = str(round(lst[0].value,2)) + ':' #init_begin_outer
		spedge += str(round(lst[1].value,2))+ ':' #actual_begin_outer
		spedge += str(round(lst[2].value,2))+ ':' #begin_error_outer
		spedge += str(round(lst[3].value,2))+ ':' #init_end_inner
		spedge += str(round(lst[4].value,2))+ ':' # actual_end_inner
		spedge += str(round(lst[5].value,2))+ ':' #end_error_inner
		system.tag.write('Path/spedge/spedge_val', spedge)
	
		tu_serID = system.tag.read('Path/TU/tu_serID').value	 
		postdata+= ';rwr_serial_id=' + str(tu_serID) 
		postdata+= ';plan_length=' +str(system.tag.read('Path/TU/CutLenSet_pts').value) 
		postdata+= ';actual_len=' + str(system.tag.read('Path/TU/take_len').value) #+ ';accum_len=43198'#;tu_color=RD;tu_status=OK;stop_code=STCT;mach_speed=1500;spoolRun=Single;I_PO_TEN=59.5:76.1:2.27:70.17;I_TU_TEN=44.2:55.5:1.92:50.18;I_PF_TEN=106.3:114.5:1.48:110.11;SPEDGE=30.54:29.91:-0.52:175.56:176.03:0.21:;DEFECT=0:0;MISC=21'
		postdata+= ';accum_len=' + str(system.tag.read('Path/TU/take_len').value) 
		postdata+= ';tu_color=' + str(system.tag.read('Path/fiber_color').value)
		postdata+= ';tu_status=OK' #+ str(system.tag.read('Path/tu_status').value) 
		
		stop_code = shared.main.Stop_code() 
		
		
		if system.tag.read('Path/TU/take_len').value <30 and (stop_code == 'PFBK'):
			stop_code = 'TUBK'	
			
		system.tag.write('Path/stop_code', stop_code)
		postdata+= ';stop_code=' + str(stop_code)
	
		postdata+= ';mach_speed=' + str(system.tag.read('Path/speed_info').value)#JIH gather avg speed
		postdata+= ';I_PO_TEN=0.0:0.0:0.0:0.0'
		postdata+= ';I_TU_TEN='+ str(system.tag.read('Path/TU/tu_ten_info').value)
		postdata+=';I_PF_TEN='+ str(system.tag.read('Path/pf_ten_info').value)
		postdata+= ';SPEDGE='+ spedge
		#SEND PITCH CHANGE PARAMETER ONLY WHEN THERE IS A PITCH CHANGE 
		if system.tag.read('Path/pitch_change').value == 1:
			postdata+= ';PITCH=' + str(system.tag.read('Path/PITCH').value) 
			
		postdata+= ';MISC=21'

		sendstring1 = shared.main.PTS_URL + svc + postdata #Sendstring2 = directive=state. get the state of the machine. 
		print sendstring1
		shared.main.log(sendstring1)
		
		
		
		response = system.net.httpGet(sendstring1)
		shared.main.log(response)
		responsesp = response.split(":") #example :770:231:COMP:TU:JRFSF3959D2CLJ:0:RACK:PAYOUT:41:SALE:0:::NONE:
		#:770(0):231(1):COMP(2):TU(3):JRFSF3959D2CLJ(4):0(5):RACK(6):PAYOUT(7):41(8):SALE(9):0(10):(11):(12):NONE(13):
		print response
		#IF PITCH CHANGE, TURN OFF THE FLAG. 
		system.tag.write('Path/pitch_change',0)
		
		#check to see if the spool is already completed. 
		#this is to avoid freeze on the sequence/handshaking when a "complete" button is already pressed on nextrom HMI 
		#error2 checks with the error given from PTS  = give nextrom the NEXT tu signal	
		error2 = str(system.tag.read('Path/TU/tu_fiberID').value) + ' has already been used in rew_fiber. :' #added 12/19/2018

		
		
		if responsesp[5] == '0'or response[6] == error2:
			system.tag.write('Path/TU/NextTU','true')
			system.tag.write('Path/TU/Next_TU_LCU','true')
			system.tag.write('Path/TU/prevent_newtu','false')
			#system.tag.write('Path/TUBK','false')
			time.sleep(2)
			system.tag.write('Path/TU/NextTU','false')
			system.tag.write('Path/TU/Next_TU_LCU','false')
			system.tag.write('Path/instruction','Completed Takeup. ' + responsesp[9])#changed from 12 JIH
			system.tag.write("Path/TU/tu_send_area", responsesp[6]) #changed from 8 JIH
			system.tag.write("Path/po_sendarea", responsesp[7])	
			system.tag.write('Path/TU/nextID', responsesp[8])#changed from 9
			system.tag.write('Path/po_next_id', responsesp[13]) #JIH for GetID
			system.tag.write('Path/TU/tu_plan_area', responsesp[9])
			system.tag.write('Path/TU/actual_len',0)
			system.tag.write('Path/TU/tu_fiberID',' ')
			
			if system.tag.read('Path/po_sendarea').value=='COMP':
				#system.tag.write('Path/po_fiberID', '')
				#system.tag.write('Path/po_serID', '')
				system.tag.write('Path/po_removeID',1)
				system.tag.write('Path/TU/nextID', '')
				system.tag.write('Path/TU/CutLenSet_pts', '')
				system.tag.write('Path/po_len_set', '')
				system.tag.write('Path/TU/tu_plan_area', '')
				system.tag.write('Path/po_serID_hidden', '')
				time.sleep(1)
				system.tag.write('Path/po_removeID',0)
		else:
			system.tag.write('Path/TU/NextTU','false')
			system.tag.write('Path/TU/Next_TU_LCU','false')
			system.tag.write('Path/instruction',responsesp[6])
	
		#system.tag.write('Path/instruction', 'Set Takeup area to %s. Set Payout area to %s',responsesp[6],responsesp[7])
		#PAYOUT
		
		res_size = responsesp.count(':')
		#previous spool HAS TO BE  completed TO ACCEPT NEW SPOOL
		system.tag.write('Path/TU/previous_completed',1)
		
		if  res_size > 7:
		
			system.tag.write("Path/ink_level", responsesp[res_size+1]) #41
			system.tag.write("Path/type_use", responsesp[res_size+2]) #SALE
		
			system.tag.write("Path/instruction", responsesp[res_size+4]+ ' ' +responsesp[res_size+5] ) #0
	
			system.tag.write("Path/nextDrawID",  responsesp[res_size+5]) #	
			
	#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
			
	
			print ("Invalid response. Check the message sent")
	except:	
		shared.main.log("CompleteTU error: "+ traceback.format_exc())
	

#		 Case "TUpdateTakeup"
#            gTuSendArea$ = TokenArray(TOKENSTART%)   'Current spool takeup send area
#            gPoSendArea$ = TokenArray(TOKENSTART% + 1)
#            gTuSpool$ = TokenArray(TOKENSTART% + 2)
#            gTypeUse$ = TokenArray(TOKENSTART% + 3)
#            gInkLevel$ = TokenArray(TOKENSTART% + 4)   'Current ink level
#            If (gfViewTrace) Then
#                objUserControl.TXT_debug_SelText = Chr$(CR) + Chr$(LF) + "UP:TU set takeup spool type to" & gTuSpool$
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 4) Then
#                gInstruction$ = TokenArray(TOKENSTART% + 5)
#                If (gInstruction$ <> "") Then Logger LOG_CLIENT, LOG_TRACE, "UP:TU set instruction to " & gInstruction$
#            Else
#                gInstruction$ = ""
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 5) Then
#                gInstruction2$ = TokenArray(TOKENSTART% + 6)
#                If (gInstruction2$ <> "") Then Logger LOG_CLIENT, LOG_TRACE, "UP:TU set instruction2 to " & gInstruction2$
#            Else
#                gInstruction2$ = ""
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 6) Then
#                gNextDrawID$ = TokenArray(TOKENSTART% + 7)
#            End If
#	PITCH CALCULATIONS 

#WHILE pitch detection is on, calculate the traverse position. 

	
	#TU DANCER TU_PKG vals 
	#TU-PKG PARAMETERS ADDED 7/18/18 PCCCC
	
	
	#while (system.tag.read('Path/test_mach_running').value == 1) and not (system.tag.read('Path/test_mach_stopped').value==1):
#	count = 0
#	#inTolerance parameters 
#	t = shared.main.inTolerance
#	num = 90 #90 degrees
#	toleranceVal = 15 #15 degrees tolerance
#	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
#	const = 1.8 #conversion contanst from percentage to degree 
#	
#	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
#	dancerPos = system.tag.readAll(dancerList)
#	
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	
	
	
	#TU-PKG PARAMETERS ADDED 7/18/18 PPC




import math 
from time import gmtime, strftime
import time



#lst = array
def stdDev(lst):
    #Calculates the standard deviation for a list of numbers.
    try:
        num_items = len(lst)
        print num_items
#        print sum(lst)
        mean = (sum(lst) / num_items)
        differences = [x - mean for x in lst]
        sq_differences = [d ** 2 for d in differences]
        ssd = sum(sq_differences)
        
        variance = ssd / num_items
        sd = math.sqrt(variance)
    except:
        sd=0
        if num_items == 0:
            print 'Standard deviation exception - Empty array'
    
    #sd = 0
    return round(sd,2)
 
def mean(lst):
    try:
        num_items = len(lst)
        mean = (sum(lst) / num_items)   
        return round(mean,2)
    except:
        mean=0
        return round(mean,2)
        
def avg(lst):
    try:
        num_items = len(lst)
        mean = (sum(lst) / num_items)   
        return mean
    except:
        mean=0
        return mean
     
# tu tension and pf tension sampling data 
#INCLUDED DANCER POS SAMPLING PPC 7/19/18
def pf_sample():#PF sample samples all data from the start 
    system.tag.write('Path/sum', 0)
    pf_ten_array=[]
    tu_ten_array=[]
    spedge_array = []
    dancerPos_array = [] #dancer Pos TU
    speed_array = []
    
    #added 12/4/18 PPC 
    #mach_start signal isn't sent to PTS until the taping is done. OR if its pressed manually. 
    #manual presssing of start is differentiated by the length of the fiber. if the length is NOT 0 or at least greater than one and then the system receieves a start signal, only then send it to PTS. 
    #this is temp fix until we can differentiate auto start from manual HMI start. 
    #
    #
    
    if (system.tag.read('Path/TU/tapingDone').value == True and system.tag.read('Path/mach_running').value ==True) or ((system.tag.read('Path/mach_start').value ==True) and (system.tag.read('Path/mach_running').value==True)):
        shared.mach_start_stop.mach_start() #send to PTS the start string
        tapingDone = 'True'
        system.tag.write('Path/mach_start_after_taping',1) #this value is set to 0 at CompleteTU event.
        
    
    #test_mach_running
    #while (system.tag.read('Path/test_mach_running').value == 1) and not (system.tag.read('Path/test_mach_stopped').value==1):
    
    #if shared.pf_sample.tapingDone == True: #to eliminate pf_Tension outliers before taping. added 2.5.19 PPC
    time.sleep(2)
            #added a delay to avoid pf_Tension outliers 
    while  (system.tag.read('Path/mach_running').value == 1) and not (system.tag.read('Path/mach_stopped').value==1):
        if system.tag.read('Path/manual_mode').value == 1:
            tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID_manual', 'Path/TU/tu_fiberID']
        else:
            tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID', 'Path/TU/tu_fiberID']
            
        list = system.tag.readAll(tagPaths)
        pf_ten = ((system.tag.read('Path/pf_ten_meas').value))
        tu_ten = ((system.tag.read('Path/TU/tu_ten_meas').value))
        speed = ((system.tag.read('Path/mach_speed').value))
        
        timestamp = (strftime("%Y-%m-%d %H:%M:%S"))
        pf_ten_array.append(pf_ten)
        tu_ten_array.append(tu_ten)
        speed_array.append(speed)
        print speed
        
        #insert into the database = ten_log ---> changed table name to tension_log 12/3/18 PPC
        system.db.runPrepUpdate("INSERT INTO tension_log (po_serialID, po_fiberID, tu_serialID, tu_rwrID, PF_TEN,TU_TEN, mach_speeds, timestamp ) VALUES (?,?,?,?,?,?,?,?)",[list[0].value,list[1].value,list[2].value,list[3].value, pf_ten, tu_ten, speed, timestamp],'mysql') 
        
        time.sleep(3)
        
        #next_value = system.tag.read('fDancerPosMe').value
        
#        if current_value == next_value:
#            count = count+1
#        else:    print 'no count'
#        print count
#        
        #next_value = system.tag.read('fDancerPosMe').value
        
#        if current_value == next_value:
#            count = count+1
#        else:    print 'no count'
#        print count
#        
#    
    s = shared.db
        
    pf_stdDev = s.stdDev(pf_ten_array)
    pf_avg = s.mean(pf_ten_array)
    
    tu_stdDev =s.stdDev(tu_ten_array)
    tu_avg = s.mean(tu_ten_array)
    speed_avg = s.avg(speed_array)

    
    try:
        x=round((min(pf_ten_array)),1)
        y=round((min(tu_ten_array)),1)
        
        a= round((max(pf_ten_array)),1)
        b=round((max(tu_ten_array)),1)
    except:
        x=0
        y=0
        a=0
        b=0
    pf_info_temp = str(x) + ':'+ str(a)+ ':' + str(pf_stdDev) + ':' + str(pf_avg )
    tu_info_temp = str(y) + ':'+ str(b) + ':' + str(tu_stdDev) +':' + str(tu_avg ) 
    system.tag.write('Path/pf_ten_info', str(pf_info_temp))
    system.tag.write('Path/TU/tu_ten_info', str(tu_info_temp))
    system.tag.write('Path/speed_info', speed_avg )
    print pf_info_temp

#4.11455059052:23.8034981092:4.77952943925:25.2021751404


import system
import traceback
import time 
import math 
from time import strftime
#THIS FUNCTION IS CALLED When Get_ID button is pressed

#send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=state;mach_no=750;oper_id=JAM
#got: 750:JAM:RWD:AUX:state:0:MUNZ JOHN A:???:???:???:???:0:???:MainRoom:CALIBRATE:ONLINE:ON:250000:250000:PAYOUT:UNCL:FIBCOLOR:??:JAM:PAYSPL:??:TAKSPL:??:TAKLEN:0:CUTLEN:0:PAYLEN:0:PROOFTEST:0:CLMODE:??:TAKTEN:???:TAKPIT:???:PAYTEN:???:DIETEN:???:ISELEN:0:MAXSPEED:0:ORDER:NO:DSM751:AIRLNTH:0:AIRDNSE:0:TWIST_V:0:TWIST:N:SEDGBGN:0:SEDGEND:0:no:TASKASGN:NO:NONE:

def GetSpool():

	try:
		PTS_URL = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
		svc = 'rewind_aux/rewind_aux.svc/process?inString=directive=state;'
		x= system.tag.read('Path/mach_no').value
		y= system.tag.read('Path/current_operid').value
		
		data = 'mach_no=' + str(x) + ';'
		data += 'oper_id=' +str(y)
	
		getSpoolSend = shared.main.PTS_URL + svc + data
		shared.main.log(getSpoolSend)
		print  shared.main.PTS_URL + svc + data
		response1 = system.net.httpGet( shared.main.PTS_URL + svc + data)
		print response1
		time.sleep(1)
		shared.main.log(response1)
		response1sp = response1.split(':')
		if response1sp[5]=='0': #response is GOOD 
			system.tag.write('Path/instruction','Machine on task assignment? ' + response1sp[67] + ', Next Draw Spool=' + response1sp[68])
			system.tag.write('Path/nextDrawID',response1sp[68])			
		else:
			system.tag.write('Path/instruction','Cannot GetID. Verify you are logged in and machine on assignment')								
	except:
		shared.main.log ('Get_ID Error: '+traceback.format_exc())	
		
	
#[2018.05.11 00:24:40] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=mach_start;start_length=23;line_speed=746;mach_no=770;oper_id=251
#[2018.05.11 00:24:40] ! VBC INET got: 770:251:RWD:AUX:mach_start:0:
import system
import traceback
import time
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/mach_running


def mach_start(): #machine start
	svc = 'rewind_aux/rewind_aux.svc/process?inString='

	
	data = 'directive=mach_start'
	data+= ';start_length=' + str(system.tag.read('Path/take_len').value)
	data+= ';line_speed=' + str(system.tag.read('Path/maxLineSpeed').value)
	data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value) #JIH read tag since sometime main value was none
	data+= ';oper_id=' + str(system.tag.read('Path/current_operid').value)

	
	try:
		sendstring1 = shared.main.PTS_URL + svc + data
		
		
		response1 = system.net.httpGet(sendstring1)
		print response1	
		shared.main.log(response1)
		
		response1sp = response1.split(':')
		
		if response1sp[5] == '0':
			system.tag.write('Path/instruction',"Machine started with no errors")
		else:
			x = "Error in starting"
			shared.main.log(x)
		

	except:
		shared.main.log('Machine Start:' + traceback.format_exc())
		
	shared.main.log(sendstring1)
		
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU	
def mach_stop():
	
#[2018.05.24 13:11:08] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=mach_stop;stop_reason=STCT;stop_length=50723;mach_no=770;oper_id=334
#[2018.05.24 13:11:08] ! VBC INET got: 770:334:RWD:AUX:mach_stop:0:
	time.sleep(0.5)
	svc = 'rewind_aux/rewind_aux.svc/process?inString='
	data = 'directive=mach_stop'
	stop_length =  str(system.tag.read('Path/TU/take_len').value)
	stop_code = shared.main.Stop_code() 
	shared.main.log(stop_code)
	system.tag.write('Path/stop_code',stop_code)	
	
	data+= ';stop_reason=' + stop_code#stop_reason
	data+= ';stop_length=' + stop_length
	data+= ';mach_no=' + '601'
	data+= ';oper_id=' + str(system.tag.read('Path/current_operid').value)
	
	#if tapingDone == True:
	sendstring1 = shared.main.PTS_URL + svc + data
	print sendstring1 
	shared.main.log(sendstring1)
	
	response1 = system.net.httpGet(sendstring1)
	print response1	
	shared.main.log(response1)
	
	response1sp = response1.split(':')
	
	#if response1sp[5] == '0': #JIH removed if statement so complete works when PTS communication did not
	system.tag.write('Path/NextTU','true')
	system.tag.write('Path/instruction', 'Machine Stopped')
	time.sleep(1)
	system.tag.write('Path/NextTU','false')
	tapingDone = False
	#else:
	#	system.tag.write('Path/NextTU','false')

	
#######################################################
#GENERAL MACH VALUES 
#######################################################
import time 

import system

mach_no = system.tag.read('Path/mach_no')

target = 'dev'

if target == 'dev':
	PTS_URL='http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
else:
	PTS_URL='http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'

from time import gmtime, strftime

timestamp = (strftime("%Y-%m-%d %H:%M:%S"))
#######################################################

from time import gmtime, strftime
import system 
import java.io as F
from java.util import Calendar

c=Calendar.getInstance()
tMs=c.getTimeInMillis()
adir = "C:\\postdraw\\"
print c.get(Calendar.DAY_OF_MONTH)
day = (c.get(Calendar.DAY_OF_MONTH)) # days 0 thru 9 have a leading 0. 
month = c.get(Calendar.MONTH)+1
if day < 10 :
	print day
	day = '0'+ str(day)
if  month < 10: 
	month = '0'+str(month)
	
filename = adir+"zlog-%d.%s.%s.txt"%(c.get(Calendar.YEAR),month,(day))
print filename

#######################################################
#SEND EMAIL
##################################################
#ileName = filePath.split("\\")[-1]

def Send_Email(temp):

	#fileData = fpmi.file.readFileAsBytes(filePath)
	if temp == 'TU_Rejects':
		subject = 'Multiple Takeup Spool Rejects' #reason code for the issue and send email for the take up spools rejected
		body = system.tag.read('Path/instruction').value
	elif (temp == 'fiberBreak') and (system.tag.read('Path/mach_running').value==0):
		subject = 'Fiber Break. Attention Required.'
		body =   'Fiber break occured on '+ str(system.tag.read('Path/mach_no').value)+'.'#str(system.tag.read('Path/stop_code').value)
	elif temp == 'tapingFail':
		subject = '601 Attention Required'
		body = 'Auto-taping Failed, Operator attention required.'
	elif temp == 'mach_idle':
		subject = '601 Machine idle'
		body = 'Machine has been idle for over 25 minutes, Operator attention required. Active PO ' + str(system.tag.read('Path/po_fiberID').value)

	smtp = "mail.ofsoptics.com"
	sender = "REW601@OFS"
	#recipients = ["pcharles@ofsoptics.com"]
	recipients = ["jheim@ofsoptics.com","pcharles@ofsoptics.com",'jmunz@ofsoptics.com','dbalfour@ofsoptics.com','twilliamson@ofsoptics.com','rflores@ofsoptics.com']
	system.net.sendEmail(smtp, sender, subject, body, 0, recipients)#, [fileName], [fileData])	
#Function to display log on the root container 

	#Function to log files on 
	########################################################
	
def writeToFile(text):
	
	line = (strftime("[%Y.%m.%d  %H:%M:%S] "))+ (text)+'\n'
	fstream = F.FileWriter(filename,1)    
	out = F.BufferedWriter(fstream)
	out.newLine()
	out.write(line)    
	out.close()
	  
y=""

def log(x):
			
	main.y = main.y + (strftime("[%Y.%m.%d   %H:%M:%S]")) + " " +x +"\n"    
	system.tag.write('displayMsg',main.y)
	writeToFile(x)
	return x


###################################################################################
#custom tolerance function. Parameter description
#returns bool. isRange = 1, not in range = 0
#test = the value you want to test. variable value. type = float
#toleranceVal = % value! the +- value, written in percentage. 
#num = constant, float, constant value 
#mode = PERCENTAGE or actual value. mode = 1 for PERCENTAGE and 0 for float tolerance value
#therefore: 10+-5% will be written as: isRange = inTolerance(10,5,testVariable)
########################################################
def inTolerance(num, toleranceVal,test,mode):

	toleranceVal = toleranceVal * 1.0 #convert to float
	if mode == 1: #if tolerance value is in percentage, convert to a float 
		x =  num * (toleranceVal/100)*1.0 #converted to float
	else:
		x=toleranceVal
	
	
	#print x
	maxVal = num + abs(x)
	minVal = num - abs(x)
	#return float(minVal), float(maxVal)
	#print minVal, maxVal
	
	if test <= maxVal and test>=minVal:
		isRange = 1
	else: 
		isRange = 0
	return isRange
#######################################################
#LOG LENGTH EVERY 5 SECONDS	
#######################################################
def logLength():
	data = 'TU SERIAL = '+ str(system.tag.read('Path/TU/tu_serialID').value)
	data+= str(system.tag.read('Path/TU/take_len').value)
	main.log(data)
	time.sleep(5)


#######################################################
	
def toggle(tagPath): #toggle values. make flags momentary
	
	temp = system.tag.read(tagPath)
	
	if temp == '1':
		system.tag.write(temp,'false')
	else:
		system.tag.write(temp,'false')


########################################################
#STOP CODE 
########################################################
def Stop_code():

				
			if (system.tag.read('Path/TUBK').value)==1:# and system.tag.read('Path/PFBK').value ==1) or (system.tag.read('Path/TUBK').value == 1):
				code = 'TUBK'
				print 'TUBK'
			elif system.tag.read('Path/PFBK').value == 1:
				code = 'PFBK'
				print 'pfbk'
				main.log('PFBK occured')
				system.tag.write('Path/instruction', 'PFBK')
			elif system.tag.read('Path/STCT').value == 1:
				code= 'STCT'
				print 'stct'
			elif system.tag.read('Path/bPOBK').value == 1:
				code = 'POBK'
				print 'pobk'
				
			else:
				code = 'PFBK'
				
			if system.tag.read('Path/TU/take_len').value < 5: #added on 2/25/19 PPC ; OPLN = auto tapingFailure
				code = 'OPLN'
				main.log('Auto taping Failure occured')
			
			
			return code
			
########################################################
#LOGOUT LOGIC 			
#######################################################

def Logout():
		   	system.tag.write('Path/operValid',0)
		   	system.tag.write('Path/oper_name',"")
		   	system.tag.write('Path/oper_id',"")
		   	system.tag.write('Path/oper_password',"")
		   	system.tag.write('Path/operValid',"false")
		   	
		   	
		   	
########################################################
#COLLECT DATA		
#######################################################
def collect_data():
	while (system.tag.read('Path/mach_running').value == 1) and not (system.tag.read('Path/mach_stopped').value==1):
		length_run = system.tag.read('Path/TU/take_len').value
		main.log('RUN LENGTH - ' + str(length_run))	
		time.sleep(7)


def ackDancer():
		system.tag.write('Path/TU/NextTU',1)
		system.tag.write('Path/TU/Next_TU_LCU',1)
		time.sleep(1)
		system.tag.write('Path/TU/NextTU',0)
		system.tag.write('Path/TU/Next_TU_LCU',0)
		system.tag.write('Path/instruction', 'Dancer Fault acknowledged, ready for the Next TU spool')
		main.log('Dancer Fault acknowledged. Ready for the Next TU spool') 
		
def Fiber_Break():
		
	main.Stop_code()
	CompleteTU.CompleteTU()
	
	TUpkg.Send_tupkg()
	system.tag.write('Path/mach_start_after_taping',0)

import threading 
def SetupTU_timer():
	print 'timer Done!'

#arg1= time in ms
#arg2 = function to execute when timer is done

def startTimer(temp):
	if temp == 'TU':
		
		threading.Timer(250, SetupTU_timer).start() #hello function will be executed after 4seconds



#Complete TU 
#triggered by "Complete" button by the PLC 
#Corresponds to TVerifyTakeup Function on NETUTIL.bas 

#COMPLETE TU		
#Example:  http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/completeTU/completeTU.svc/process?inString=mach_no=770;oper_id=117;
#po_id=JRFVY3889A1RVJ;po_serial_id=3800125904;rwr_id=RWR551295121;rwr_serial_id=5206475492;
#plan_length=50550;actual_len=50551;accum_len=50555;tu_color=GR;tu_status=OK;stop_code=STCT;
#mach_speed=1500;spoolRun=Single;I_PO_TEN=66.5:72.7:1.45:69.48;I_TU_TEN=45.4:55.3:1.83:49.78;
#I_PF_TEN=106.1:114.7:1.82:109.75;SPEDGE=30.54:29.77:-0.49:175.56:176.35:0.39:;DEFECT=0:0;MISC=21
import system 
import time
import threading
def manualComplete(temp):
	if temp == 'opln':
		t = threading.Timer(600,shared.main.Send_Email('tapingFail'))
		t.start()
	elif temp == 'tubk' or 'pfbk' or 'pobk':
		t = threading.Timer(600,shared.main.Send_Email('fiberBreak'))
		t.start()
		print 'send email'
	shared.CompleteTU.CompleteTU()
	shared.TUpkg.Send_tupkg()
	system.tag.write('Path/TU/previous_completed',1)
	if temp == 'auto':
		shared.main.log('Spool auto completed')
	else:
		shared.main.log('Spool manually completed')
	
#	system.tag.write('Path/TU/Next_TU_LCU',1) #added this to complete no matter what
#	system.tag.write('Path/TU/NextTU',1)
#	time.sleep(1.5)
#	system.tag.write('Path/TU/Next_TU_LCU',0) #added this to complete no matter what
#	system.tag.write('Path/TU/NextTU',0)
	

print 'hello'
import time
import math
#operator login function, that passes the PTS Url and service. Maybe change later 
import traceback

#def a function at each state. directive or state of the machine 
#directive=Logon 
#for sale spools, not Tspool, you logon at every instance. 
#PTS_URL = "http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/"


# (Path/OperLogonReady) = Ready to run the _1_Oper_Logon script
def SendURL(URL,svc,data):
	send_data = URL + svc + data
	
	return send_data


#Oper Logon send event 
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/OperLogonReady
def Logon():
#dev PTS_URL. change for prod
	
	svc = "rewind_aux/rewind_aux.svc/process?inString="	
	directive1 = "oper_logon"
	mach_no = system.tag.read("Path/mach_no")
	if system.tag.read("Path/bTrue4").value == True: #JIH option to login through Ignition
		oper_id = system.tag.read("Path/layout_id")
		if len(system.tag.read("Path/layout_id").value) == 5:
			oper_pw = "BadgeNb"
		else:
			oper_pw = system.tag.read("Path/layout_pw") #'BadgeNb'
	else:
		oper_id = system.tag.read("Path/oper_id")
		if len(system.tag.read("Path/oper_id").value) == 5:
			oper_pw = "BadgeNb"
		else:
			oper_pw = system.tag.read("Path/oper_password").value #'BadgeNb'
	#layout_id = "XXX"
	#layout_passwd = "XXXXXX"
	
	postData = "directive=" + directive1 +';' 
	postData += 'mach_no=' + str(mach_no.value) + ';'
	postData += 'oper_id=' + str(oper_id.value.upper()) + ';'
	if system.tag.read("Path/bTrue4").value == True:
		if len(system.tag.read("Path/layout_id").value) == 3:
			postData += 'oper_passwd=' + str(oper_pw.value).upper()
		else:
			postData += 'oper_passwd=' + oper_pw	
	else:
		if len(system.tag.read("Path/oper_id").value) == 3:
			postData += 'oper_passwd=' + str(oper_pw.value).upper()
		else:
			postData += 'oper_passwd=' + oper_pw
	sendstring1 = SendURL(shared.main.PTS_URL,svc,postData)#PTS_URL + svc + postData #sendstring1 is directive=oper_logon
	print sendstring1
	shared.main.log(sendstring1)
	
	try:#send string to get a response
		
		response1 = system.net.httpGet(sendstring1)
		response1 = system.net.httpGet(sendstring1)
		print response1
		shared.main.log(response1)
	
		
		loginResponseSp = response1.split(":") #response split to get members of the array
	
			
		if loginResponseSp[5] == "0":
			operlogonValid = 1 #binary
			 #valid =0 invalid <>0
			system.tag.write("Path/operValid",operlogonValid) #binary logon valid
			system.tag.write('Path/instruction', 'Operator Logged in: ' + str(system.tag.read('Path/oper_name').value))
			
	
			#########################################################################################int
			
		#quantify inital login. Logout itself after a while 
		#machine stop code = 05 Check the code
		#check for state at every login
			directive2 = "state"
			postData2= "directive=" + directive2 +';' 
			postData2+= 'mach_no=' + str(mach_no.value) + ';'
			postData2+= 'oper_id=' + str(oper_id.value)
			
			sendstring2 = shared.main.PTS_URL + svc + postData2 #Sendstring2 = directive=state. get the state of the machine. 
			shared.main.log(sendstring2)
			stateRes= system.net.httpGet(sendstring2)
			shared.main.log(stateRes)
			 
			
			stateRessp = stateRes.split(':') #StateRes Split - State Response Split 
			#print stateRes
			
	
			if stateRessp[5] == '0': #check for validity 
				system.tag.write('Path/stateResValid',1)
				system.tag.write('Path/instruction', stateRessp[6])
				system.tag.write('Path/po_type',stateRessp[7])
				print stateRes
				
			
			else: 
				system.tag.write('Path/stateResValid',0)
				system.tag.write('Path/instruction',stateRessp[6]+'. '+stateRessp[7])	
				shared.main.log(stateRessp[6]+'. '+stateRessp[7])
				#TEST print 
				
			
			#770:231:RWD:AUX:state:0:HORN JOHN:???:???:???:???:-2:???:MainRoom:CALIBRATE:ONLINE:ON:0:250000:PAYOUT:UNCL:FIBCOLOR:??:231:PAYSPL:??:TAKSPL:??:TAKLEN:0:CUTLEN:0:PAYLEN:0:PROOFTEST:0:CLMODE:??:TAKTEN:???:TAKPIT:???:PAYTEN:???:DIETEN:???:ISELEN:0:MAXSPEED:0:ORDER:NO:DSM751:AIRLNTH:0:AIRDNSE:0:TWIST_V:0:TWIST:N:SEDGBGN:0:SEDGEND:0:no:TASKASGN:NO:NONE:
				
					
			size_stateRes = stateRes.count(':')
					
			
		#SEE LINE 154 FOR DETAILS.	
		#INTERMEDIATE VALUE TAGS FROM EXCEL SHEET
			system.tag.write("Path/mach_no", stateRessp[0])          #
			system.tag.write("Path/oper_id", stateRessp[1])          #
			#system.tag.write("Path/valid", stateRessp[5])          #
			system.tag.write("Path/oper_name", stateRessp[6])          #
			system.tag.write("Path/po_fiberID", stateRessp[7])          #
			system.tag.write("Path/po_serID", stateRessp[8])          #
			system.tag.write("Path/TU/tu_fiberID", stateRessp[9])          #
			system.tag.write("Path/TU/tu_serID", stateRessp[10])          #
			system.tag.write("Path/PayoutLenSofar", stateRessp[11])          #
			#system.tag.write("Path/DieID", stateRessp[12]) 
			if stateRessp[14] == 'CALIBRATE':
				system.tag.write('Path/instruction','Check Calibration of the machine')         #
			system.tag.write("Path/maxInkLevel", stateRessp[18])          #
			system.tag.write("Path/po_sendarea", stateRessp[19])          #
			#system.tag.write("Path/Current_color", stateRessp[20])          #
			#system.tag.write("Path/fiber_color", stateRessp[22])          #
			system.tag.write("Path/current_operid", stateRessp[23])          #
			system.tag.write("Path/po_type", stateRessp[25])          #
			system.tag.write("Path/TU/tu_type", stateRessp[27])          #
			system.tag.write("Path/po_len_set", stateRessp[33])          #
			#system.tag.write("Path/colormode_pts", stateRessp[37])          #
			#system.tag.write("Path/TU/tu_ten_pts", stateRessp[39])          #takeup tension set point
			#system.tag.write("Path/TU/tu_pit_pts", stateRessp[41])          #takeup pit set point
			system.tag.write("Path/payTen_pts", stateRessp[43])          #Pay tension setpoint
			#system.tag.write("Path/preDie_pts", stateRessp[45])          #Pre die set point pts
			system.tag.write("Path/inEdge", stateRessp[47])          #in length set
			system.tag.write("Path/maxLineSpeed", stateRessp[49])          #max line speed
			system.tag.write("Path/ordermode", stateRessp[51])          #
			#system.tag.write("Path/inkType", stateRessp[52]) #NA for 601          #gInkType
			#system.tag.write("Path/airLen", stateRessp[54])  #NA for 601         #gAirLength
			#system.tag.write("Path/airDense", stateRessp[56])  #NA for 601         #gAirDense
			#system.tag.write("Path/twistVal", stateRessp[58])          #twist value
			#system.tag.write("Path/setTwist", stateRessp[60])          #gSetTwist
			system.tag.write("Path/edgeBegin", stateRessp[62])          #
			system.tag.write("Path/edgeEnd", stateRessp[64])          #gEndEdge
			system.tag.write("Path/meGranted", stateRessp[65])          #MUTLIPLE end granted?
			system.tag.write("Path/task_asgn", stateRessp[67])          #task assigned
			system.tag.write("Path/nextDrawID", stateRessp[68])          #
			#system.tag.write("Path/dualspool", stateRessp[70])          #
			system.tag.write('Path/bTrue4',0)
			
		else:
			system.tag.write('Path/instruction',loginResponseSp[5])
			
			if loginResponseSp.count(':') > 5:
			
				shared.main.log(loginResponseSp[loginResponseSp.count(':')+1])
			
	except: 
		shared.main.log ('Operator Login Error'+traceback.format_exc())





def OperLogout():

	print 'logout'
	import time
	import system
	system.tag.write('Path/test_start','true')
	time.sleep(4)
	system.tag.write('Path/test_false','false')



import system
import time
import traceback
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/po_setup
def SetupPO():

	system.tag.write('Path/po_removeID',0)
#VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/setupPO/setupPO.svc/process?inString=701:128:JRFVY1714A1RVH:3800117787:DEF_DET:NO:DEF_LVL:0::
#VBC INET got: 701:128:SETUP:PO:JRFVY1714A1RVH:0:TAKEUP:41:SALE:200M:PLN:4741::
#VBC INET got: 701_0:128_1:SETUP_2:PO_3:JRFVY1714A1RVH_4:0_5:TAKEUP_6:41_7:SALE_8:200M_9:PLN_10:4741_11::
	try:
		PTS_URL = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
		svc = "setupPO/setupPO.svc/process?inString="
		
		manual_mode = system.tag.read('Path/manual_mode')	
		if manual_mode.value == 1:
			shared.main.log('Machine is in manual mode')
			
		x= system.tag.read('Path/mach_no').value
		y= system.tag.read('Path/oper_id').value
		z= system.tag.read('Path/po_fiberID').value
		a= system.tag.read('Path/po_serID').value
		#hide po serial ID from operators on the HMI
		hiddenFigures = a[0] + a[1]+a[2]+a[3]+'xxxx'+a[8]+a[9]
		system.tag.write('Path/po_serID_hidden',hiddenFigures)
		
		
		data = str(x) + ':'
		data += str(y)+':'
		data += str(z)+':'
		data += str(a)+':'
		data += 'DEF_DET:NO:DEF_LVL:0:'+':' #N/A for nextrom machines
		setupPOsend = shared.main.PTS_URL + svc + data
		shared.main.log(setupPOsend)
		print  shared.main.PTS_URL + svc + data
		response1 = system.net.httpGet( shared.main.PTS_URL + svc + data)
		print response1
		time.sleep(1)
		shared.main.log(response1)
		response1sp = response1.split(':')
		
#VBC INET got: 701_0:128_1:SETUP_2:PO_3:JRFVY1714A1RVH_4:0_5:TAKEUP_6:41_7:SALE_8:200M_9:PLN_10:4741_11::	
		if response1sp[5]=='0': #response is GOOD 
			system.tag.write('Path/instruction','Payout Spool accepted . ' + response1sp[12])
			
			system.tag.write('Path/po_type',response1sp[6])
			system.tag.write('Path/po_sendarea',response1sp[7])
			system.tag.write('Path/tu_plan_area',response1sp[8])
			#system.tag.write('Path/get_setup_direction',response1sp[8])
			system.tag.write('Path/PayoutLenSofar',response1sp[11])
			shared.main.log('PO Response valid')
			
			system.tag.write('Path/po_spool_accept','true')
			time.sleep(1)	
			system.tag.write('Path/po_spool_accept','false')
			
		else:
			system.tag.write('Path/instruction','Payout Spool REJECTED. '+response1sp[6]+response1sp[7])
			system.tag.write('Path/po_spool_reject','true')
			time.sleep(1)
			system.tag.write('Path/po_spool_reject','false')
	except:
		shared.main.log ('PO Setup Error: '+traceback.format_exc())
			

#change log 


#1.22.18 error handling for cannot use regular id, enter rwrscrap

####################################################################################################
#Setup TU 
#this is followed after oper_logon, state
import system
import traceback
import time 
import math 
from time import strftime
import threading 
import main 
#example:
#[2018.05.16 20:31:50] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/setupTU/setupTU.svc/process?inString=mach_no=770:oper_id=328:rwr_id=GET_SPOOL_ID:rwr_serial_id=5220070639:sfo_final_color=NONE:;spoolRun=Single
#[2018.05.16 20:31:51] ! VBC INET got: 770:328:SETUP:TU:RWR865623657:0:PAYSPL:38:TAkSPL:52:TAKLEN:0:CUTLEN:50800:PAYLEN:306902:PROOFTEST:100:CLMODE:NONE:COLOR:OR:TAKTEN:45:TAKPIT:0.5:PAYTEN:70:DIETEN:70:ISELEN:10:MAXSPEED:1500:PLANSEND:SALE:NO:INKTYPE:NONE:TWIST_V:0:TWIST:N:AIRLNTH:0:AIRDNSE:0:SEDGBGN:30.54:SEDGEND:175.56:no:BTLIMIT:15::
#
def timerDone():
	#system.tag.write('Path/timerDone',1)
	system.tag.write('Path/TEST/bool_test',True)
	print 'timer done'
	
	


system.tag.write("Path/TU/tu_danc_bar", 0.22)
Setupsvc = 'setupTU/setupTU.svc/process?inString='#SETUP Svc 

#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/TU/tu_setup 
def SetupTU():
	#CHECK TO SEE IF THE PREVIOUS TU SPOOL IS COMPLETED 
 	previous_complete = system.tag.read('Path/TU/previous_completed').value
 	if previous_complete == 1:
 		system.tag.write('Path/instruction','Ready for a new TU spool')
 		system.tag.write('Path/TU/previous_completed',0)
	
 #reset ALL at new spool 
		TUpkg.Reset()

		
	
	###ASSEMBLE AND SEND
		system.tag.write('Path/CladdingDiameter',0.125)
		mach_no = system.tag.read("Path/mach_no")
		oper_id = system.tag.read("Path/oper_id")
		manual_mode = system.tag.read('Path/manual_mode')
		
		if manual_mode.value == 1:
			tu_serID = system.tag.read('Path/TU/tu_serID_manual').value
			system.tag.write('Path/bTrue5', 0)
		else:
			tu_serID = system.tag.read('Path/TU/tu_serID').value	
			
		system.tag.write('Path/TU/tu_serID',tu_serID) 
		
		
		
		postdata = 'mach_no=' + str(mach_no.value)
		postdata += ':oper_id=' + str(oper_id.value).upper() 
		if system.tag.read('Path/TU/tu_plan_area').value=='SCRP':#or system.tag.read('Path/TU/tu_send_area').value == 'SCRP':
			rwr_id = 'RWRSCRAP'
			system.tag.write('Path/TU/tu_fiberID','RWRSCRAP')
			#system.tag.write('Path/TU/nextID','')#reset next TU ID
			
		#elif system.tag.read('Path/nextDrawID').value == 'SCRP':
			#rwr_id='RWRSCRAP' 
			#system.tag.write('Path/nextDrawID',"")
		else:
			rwr_id = 'GET_SPOOL_ID'
			
		postdata+= ':rwr_id='+ str(rwr_id)
		postdata+= ':rwr_serial_id=' + str(tu_serID)
		postdata+= ':sfo_final_color=' + 'NONE'
		postdata+= ':;spoolRun=' + 'Single'
		###############################################################
		#SEND TO PTS
		try:
			sendstring1= OperLogon.SendURL(main.PTS_URL, Setupsvc, postdata)
			print sendstring1
			main.log(sendstring1)
			#RESET TU_PLAN_AREA from previous completeTU instruction. Example: if instruction from previous completeTU is "RWRSCRP", reset it as soon as takeup
						
		except:
			main.log(traceback.print_exc('sendstring1'))
			
			main.log ('SETUP TU Error'+traceback.format_exc())
	
		
		### PARSE RESPONSE
		#######################################################################
		#RESPONSE FROM PTS
		try:
			time.sleep(1)
			response1 = system.net.httpGet(sendstring1)
			print response1
			main.log(response1)
			response1sp = response1.split(':')
		
			#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
			
			if response1sp[5]=='0': #response is GOOD 	
				
	#		for i in range(0,response1.count(':')+1):
	#			print ('%d = ')%i + response1sp[i]
				system.tag.write('Path/instruction',response1sp[6])
				#system.tag.write("Path/oper_id", response1sp[1])          #
				phase = response1sp[2] + response1sp[3]
				system.tag.write('Path/TU/tu_fiberID',response1sp[4])
				system.tag.write("Path/setupValid", response1sp[5])      
				system.tag.write("Path/po_type", response1sp[7])          #
				system.tag.write("Path/TU/tu_type", response1sp[9])          #
				system.tag.write('Path/TU/tuLenSet_pts', float(response1sp[11]))
				system.tag.write('Path/TU/CutLenSet_pts', float(response1sp[13]))
				system.tag.write("Path/po_len_set", float(response1sp[15]))
				
				#MADE THE PT POINT TO 105 TO ENSURE IT STAYS ABOVE 100. PPC 8/1/18, set to 30 for scrap
						
				if response1sp[17] =='0':
					pfsetpoint = 30 		
				else:
					pfsetpoint = float(response1sp[17])+5
					
			
				system.tag.write('Path/Pfsetpoint_pts',pfsetpoint)         #
				   
				system.tag.write("Path/fiber_color", response1sp[21])         #
				system.tag.write("Path/TU/tu_ten_pts", response1sp[23])          #takeup tension set point
				system.tag.write("Path/TU/tu_pit_pts", 0.55)#response1sp[25])          #takeup pit set point
				system.tag.write("Path/TU/tu_danc_bar", 0.22)
				system.tag.write("Path/payTen_pts", response1sp[27])          #Pay tension setpoint
				system.tag.write("Path/preDie_pts", response1sp[29])          #Pre die set point pts
				system.tag.write("Path/inEdge", response1sp[31])          #in length set
				system.tag.write("Path/maxLineSpeed", response1sp[33])  #mach line speed
				#system.tag.write("Path/maxLineSpeed", 2000)  #mach line speed
				system.tag.write('Path/plan_send', response1sp[35]) #plan send or type use
				system.tag.write('Path/circle', response1sp[36])  #added new tag  
				#system.tag.write("Path/inkType", response1sp[38]) #N/A         #gInkType
#				system.tag.write("Path/twistVal", response1sp[40])          #twist value #KEY=TWIST_V
#				system.tag.write("Path/setTwist", response1sp[42])   #TWIST #gSetTwist
	#			system.tag.write("Path/airLen", response1sp[44])#N/A          #gAirLength KEY =  AIRLNTH
	#			system.tag.write("Path/airDense", response1sp[46]) #N/A         #gAirDense #  KEY =  AIRDNSE
				system.tag.write("Path/edgeBegin", response1sp[48])          #
				system.tag.write("Path/edgeEnd", response1sp[50])         #gEndEdge
				system.tag.write("Path/meGranted", response1sp[51])
				          #MUTLIPLE end granted?
				system.tag.write("Path/instruction", 'TAKEUP SPOOL VALID')  
				main.log('TAKEUP SPOOL VALID')   

				system.tag.write('Path/inEdge',10.0)
				system.tag.write('Path/TU/tu_spool_accept','true')
				time.sleep(1)
				system.tag.write('Path/TU/tu_spool_accept','false')
				system.tag.write('Path/TU/nextID','')#reset next TU ID, moved to after spool accepted 20180813
				system.tag.write('Path/nextDrawID',"")
				system.tag.write('Path/TU/tu_serID_PTS',tu_serID)
				system.tag.write('Path/TU/prevent_newtu','true')


				#RESET  tu spool_send area-only clear if the response back is 0
				#system.tag.write('Path/TU/tu_send_area',"")
				#system.tag.write('Path/TU/tu_plan_area',"")
				#RESET PREVIOUS SPOOL data
				tags= ["Path/TU/tu_ten_info","Path/pf_ten_info",'Path/stop_code','Path/spedge/spedge_val','Path/TU/tupkg_data','Path/Spedge/spedge_val']
				values=['0','0','none','0','0',0]
				system.tag.writeAll(tags,values)
				
								     #task assigned
				#start timer here, if tu spool is valid and doesn't run after a set amount of time, notify the operator/coach/engrs
#				timeinSec = 400
#				timer = threading.Timer(timeinSec, main.Send_Email('mach_stalled'))
#				timer.start()
#				for i in range(1,timeinSec):
#					i=i+1
#					time.sleep(1)
#					system.tag.write('Path/TEST/test_int',i)#to chck if timer is working
#					
#				
				
				#check to see if dancer is open and then complete the spool
	
			
			else:
			#if plan_send instruction from PO setup gets cleared out, and rwrscrap instruction is to be made, 
			#set the next spool for rwrscrap
				if response1sp[6] == 'Cannot use regular RWR id. Enter RWRSCRAP. ':
					system.tag.write('Path/TU/tu_plan_area','SCRP')
					#system.tag.write('Path/TU/tu_fiberID','RWRSCRAP')
				
				elif (response1sp[6] == 'Cannot use RWRSCRAP. Enter a regular RWR id.'):
					system.tag.write('Path/TU/tu_plan_area','')
				 
				
				system.tag.write('Path/instruction', 'Takeup Spool Rejected. '  + response1sp[6]) 
				main.log('Takeup Spool is Rejected. ' + response1sp[6])

				#error handling for cannot use regular id, enter rwrscrap #ppc 1.22.19



				system.tag.write('Path/TU/tu_spool_reject','true')
				system.tag.write('Path/TU/previous_completed','true')#READY TO ACCEPT A NEW SPOOL SIGNAL 
				time.sleep(1)
				system.tag.write('Path/TU/tu_spool_reject','false')
				main.log(response1sp[6])

				
				
		except:
			main.log(traceback.format_exc())
			
			#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
		
	
	else:
		system.tag.write('Path/instruction','Previous spool has to be completed to continue')
		main.log('Previous spool has to be completed to continue')	



#Case "TSendTUPackageData"
#		            OutBuff$ = GetTUPackageData$()
#		            ServerProgram$ = "pd_rema"
#		            SendString$ = gMachineNumber$ + ":" + gOperatorID$ + ":RE:MA:TUPKG:" + gTakeupID$ + ":" + gTakeupSerID$ + ":" + gMachStop$ + ":" + gLengthRun$ + ":" + OutBuff$ + ":"
#		            sendstring2$ = "directive=tupkg"
#		            sendstring2$ = sendstring2$ + ";mach_no=" + gMachineNumber$
#		            sendstring2$ = sendstring2$ + ";oper_id=" + gOperatorID$
#		            sendstring2$ = sendstring2$ + ";rwr_id=" + gTakeupID$
#		            sendstring2$ = sendstring2$ + ";rwr_serial_id=" + gTakeupSerID$
#		            sendstring2$ = sendstring2$ + ";mach_stop=" + gMachStop$
#		            sendstring2$ = sendstring2$ + ";length_run=" + gLengthRun$
#		            sendstring2$ = sendstring2$ + ";tupkg_data=" + OutBuff$

#	       '''gPoSol$ = TokenArray(TOKENSTART% + 1)             'Payout spool type
#            gTuSpool$ = TokenArray(TOKENSTART% + 3)             'Takeup spool type
#            gTuLenSet$ = TokenArray(TOKENSTART% + 5)            'Length on takeup spool
#            If Val(gTuLenSet$) > 0 Then
#                gWindMode$ = "SPLICE"
#            End If
#            gCutLenSet$ = TokenArray(TOKENSTART% + 7)           'Cut length
#            gPayLenSet$ = TokenArray(TOKENSTART% + 9)           'Payout spool length
#            gPayLen& = Val(gPayLenSet$)
#            gPrfTenSetpoint$ = TokenArray(TOKENSTART% + 11)     'Prooftest setpoint
#'            If Val(gPrfTenSetpoint$) > 35 And gTakeupID$ <> "RWRSCRAP" Then
#            If Val(gPrfTenSetpoint$) > 35 Then
#                gWindMode$ = "PROOFTEST"
#            Else
#                gWindMode$ = "REWIND"
#                gPrfTenSetpoint$ = "25"     'Set minimum to 25 kpsi per Trey Ryan 03/17/2005
#            End If
#            gColorMode$ = TokenArray(TOKENSTART% + 13)      'Color mode
#            If gColorMode = "RECU" Then
#                gColorMode = "RECURE"
#            End If
#            gFiberColor$ = TokenArray(TOKENSTART% + 15)     'Color of fiber after rewind/coloring
#            If gTakeupID = "RWRSCRAP" Then
#                gColorMode = "NONE"
#            End If
#            gTakeTenSetpoint$ = TokenArray(TOKENSTART% + 17)    'Takeup tension setpoint
#            gTakePitSetpoint$ = TokenArray(TOKENSTART% + 19)    'Takeup pitch
#            gPayTenSetpoint$ = TokenArray(TOKENSTART% + 21)     'Payout tension
#            gPreDieSetpoint$ = TokenArray(TOKENSTART% + 23)     'Pre-die tension
#            gInLenSet$ = TokenArray(TOKENSTART% + 25)           'Inside end length
#            gMaxLineSpeed$ = TokenArray(TOKENSTART% + 27)       'Fast line speed
#            gTypeUse$ = TokenArray(TOKENSTART% + 29)            'Plan Send or current takeup spool
#            gCircle$ = TokenArray(TOKENSTART% + 30)
#            gInkType$ = TokenArray(TOKENSTART% + 32)            'Ink type for DSM or Hexion
#            gTwistValue$ = TokenArray(TOKENSTART% + 34)         'Twist value
#            gSetTwist$ = TokenArray(TOKENSTART% + 36)           'Flag for setting twist value
#            gAirLength$ = TokenArray(TOKENSTART% + 38)
#            gAirDense$ = TokenArray(TOKENSTART% + 40)
#            gBeginEdge = TokenArray(TOKENSTART% + 42)
#            gEndEdge = TokenArray(TOKENSTART% + 44)
#            gMEGranted$ = TokenArray(TOKENSTART% + 45)
#            gInstruction$ = ""
#            gInstruction$ = TokenArray(TOKENSTART% + 48)
#            '''	
#	
def x():
	timer = threading.Timer(5,SetupTU.timerDone)
	timer.start()
#	
#	
	

import time
import traceback
begin_array = []
end_array = []
count = 0.0


#THIS FUNCTION CALCULATES STAE COUNT 
#THIS FUNCTION IS CALLED in  TUpkg.Calc_tupkg(parameter)

def stae(param):
		ref = TUpkg
		t = main.inTolerance
		c = main
		#inTolerance parameters
		num = 90 #90 degrees
		toleranceVal = 15 #15 degrees tolerance
		mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
		const = 1.8 #conversion contanst from percentage to degree 
		
	#	convert_val. NEXTROM prooftesters dancer position is in %. percent is converted to degrees to match BAM controllers. 
		converted_val = round(param* const,2)
#		if param == x:
#			param = system.tag.read('Path/test_float').value
#	
	#FOR STAE COUNT  CHECK IF THE DANCER POSITIONS FALL WITHIN THE TOLERANCE VALUE. This is compared against the BAM controllers - changed to degrees
		if not t(num,toleranceVal,converted_val,mode):
			TUpkg.count +=1
		system.tag.write('Path/TU/stae_count' , TUpkg.count)
		return TUpkg.count
		
#CALLED EVERY TIME THERES A TAG CHANGE IN DANCER BEGIN/END MIN/MAX POSITIONS

def Calc_tupkg(param):	

	#short hand INITIALIZE
	ref = TUpkg
	t = main.inTolerance
	c = main
	#inTolerance parameters
	num = 90 #90 degrees
	toleranceVal = 15 #15 degrees tolerance
	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
	const = 1.8 #conversion contanst from percentage to degree 
	
	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
	
	dancerPos = system.tag.readAll(dancerList)
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	d0 = round(dancerPos[0].value * const,2)
	print d0
	d1 = dancerPos[1].value * const
	d2 = dancerPos[2].value * const
	d3 = dancerPos[3].value * const
	
	#PPC 07.24.18
	#SUBTRACT 50 TO SEND TO PTS 

	#ref = what is to be calculated. 
	#this function is called at value change at each of the following paths

#	d0 = ('Path/TU/fDancerBeginMaxPos').value
#	d1 = ('Path/TU/fDancerBeginMinPos').value 
#	d2 = ('Path/TU/fDancerEndMaxPos').value
#	d3 = ('Path/TU/fDancerEndMinPos').value
	
	
#CHECK WHAT PARAMETERS ARE PASSED IN. 
	if param == 'beginMax':
		ref.begin_array.append(d0)
		
	elif param == 'beginMin':
		ref.begin_array.append(d1)
		
	elif param == 'endMax':
		ref.end_array.append(d2)
	
	elif param == 'endMin':
		ref.end_array.append(d3)
	else:
		ref.end_array.append(system.tag.read('Path/test_float').value)
		print ref.end_array
	print 'begin stdDev'
			
#	begin_stdDev = db.stdDev(ref.begin_array)
#		
#	begin_avg = db.mean(ref.begin_array)
#	begin_avg = num - begin_avg #subtract from 90 to send to PTS
#	
#	end_stdDev = db.stdDev(ref.end_array)
#
#	
#	end_avg = db.mean(ref.end_array)
#	end_avg = num - end_avg
	
	#subract everything by 90
	d0 = num - d0
	d1 = num - d1	
	d2 = num - d2	
	d3 = num - d3	


	system.tag.write('Path/TU/begin_array', ref.begin_array)
	system.tag.write('Path/TU/end_array',  ref.end_array)

	
		
	if system.tag.read('Path/manual_mode').value == 1:
		tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID_manual', 'Path/TU/tu_fiberID']
	else:
		tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID', 'Path/TU/tu_fiberID']
	
	lst = system.tag.readAll(tagPaths)
	
	#COMMENTED OUT ON 11/29/18 PPC - INSERT BACK IN. mySQL is offline
	system.db.runPrepUpdate("INSERT INTO dancerPos (beginMax, beginMin, endMax, endMin, po_fiberID, po_serialID, timestamp, tu_serialID)  VALUES (?,?,?,?,?,?,?,?)",[str(d0), str(d1), str(d2),str(d3),lst[0].value,lst[1].value,c.timestamp, lst[2].value],'mysql') 
		
		
	

	 
def Reset():#THIS FUNCTION IS CALLED AT TUpkg.Send_tupkg()
		
		TUpkg.end_array = []
		TUpkg.begin_array = []
		TUpkg.count = 0
		system.tag.write('Path/TU/stae_count',0)
		system.tag.write('Path/TU/tu_ten_info','')
		system.tag.write('Path/TU/take_len',0)
		system.tag.write('Path/TU/tu_length',0)
			

		system.tag.write('Path/TU/begin_array',[])
		system.tag.write('Path/TU/end_array',[])
		
		system.tag.write('Path/PITCH','')
		
		print TUpkg.begin_array
		
		

def Send_tupkg(): #THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU

	t = main.inTolerance
	c = main
	ref = TUpkg
	#inTolerance parameters
	num = 90 #90 degrees
	toleranceVal = 15 #15 degrees tolerance
	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
	const = 1.8 #conversion contanst from percentage to degree 
	
	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
	
	dancerPos = system.tag.readAll(dancerList)
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	d0 = round(dancerPos[0].value * const,2)
	print d0
	d1 = dancerPos[1].value * const
	d2 = dancerPos[2].value * const
	d3 = dancerPos[3].value * const
	
	
	
	begin_stdDev = db.stdDev(system.tag.read('Path/TU/begin_array').value)
	
	begin_avg = db.mean(system.tag.read('Path/TU/begin_array').value)
	begin_avg = num - begin_avg #subtract from 90 to send to PTS
	
	end_stdDev = db.stdDev(system.tag.read('Path/TU/end_array').value)
	
	
	end_avg = db.mean(system.tag.read('Path/TU/end_array').value)
	end_avg = num - end_avg
	
	#subract everything by 90
	#begin_avg= num - begin_avg
	#end_avg= num - end_avg
	d0 = num - d0
	d1 = num - d1	
	d2 = num - d2	
	d3 = num - d3
	d4 = system.tag.read('Path/Spedge/begin_error_outer').value
	d5 = system.tag.read('Path/Spedge/end_error_inner').value

	print ref.begin_array
	print ref.end_array
	
	
	
	#ASSEMBLE TU_PKG AND WRITE TO PATH/TU/TU_DATA
	tu_pkg =  str(round(begin_avg,2))+':' #fDancerBeginMaxPos
	tu_pkg += str(begin_stdDev)+':' #
	tu_pkg += str(round(d0,2))+':'#fDancerBeginMaxPos
	tu_pkg += str(round(d1,2))+':' #fDancerBeginMinPos
	tu_pkg += str(round(end_avg,2))+':'
	tu_pkg += str(round(end_stdDev,2))+':'
	tu_pkg += str(round(d2,2))+':'#fDancerendMaxPos
	tu_pkg += str(round(d3,2))+':'#fDancerendMinPos
	tu_pkg += str(round(d4,2))+':' #begin error outer
	tu_pkg +=str(round(d5,2))+':' #begin error inner
	
	
	if TUpkg.count > 0: #Last attribute of the string 
		tu_pkg += str(TUpkg.count-1)+'0'
	else:
		tu_pkg += '0.00'
		

	system.tag.write('Path/TU/tupkg_data',(tu_pkg))

	
	print tu_pkg
	#ASSEMBLE DATA AND SEND TO PTS
	try:
		svc= "rewind_aux/rewind_aux.svc/process?inString="	 #TU Svc 
		stop_code = system.tag.read('Path/stop_code') 
		manual_mode = system.tag.read('Path/manual_mode')				
		if manual_mode.value == 1:
			tu_serID = system.tag.read('Path/TU/tu_serID_manual').value
			main.log('Machine is in manual mode')
		else:
			tu_serID = system.tag.read('Path/TU/tu_serID_PTS').value	
			
		postdata= "directive=" + 'tupkg' +';' 	
		postdata+= 'mach_no=' + str(system.tag.read('Path/mach_no').value) 
		postdata+= ';oper_id=' + str(system.tag.read('Path/current_operid').value).upper()			
		postdata+= ';rwr_id=' + str(system.tag.read('Path/TU/tu_fiberID').value)#change to  
		postdata+= ';rwr_serial_id=' + str(tu_serID)		
		postdata+= ';mach_stop=' + str(system.tag.read('Path/stop_code').value)
		postdata+= ';length_run='+str(system.tag.read('Path/TU/tu_length').value)
		postdata+= ';tupkg_data='+tu_pkg
		
		
		time.sleep(1) # delay the PTS messange sending for one minute to avoid server hangup
		sendstring = main.PTS_URL + svc + postdata
		main.log(sendstring)
		#RESPONSE GET
		response = system.net.httpGet(sendstring)
		main.log(response)
		responsesp = response.split(":") #example :770:231:COMP:TU:JRFSF3959D2CLJ:0:RACK:PAYOUT:41:SALE:0:::NONE:
		if responsesp[5] == '0':
			ref.Reset()
			#system.tag.write('Path/instruction','TU spool completed, place it on the RACK')
		else:
			system.tag.write('Path/instruction',responsesp[6])
			
		main.log('TUpkg data = ' + tu_pkg)
		ref.tu_pkg = tu_pkg
		
		
	except:
		main.log('Tupkg exception: ' + traceback.format_exc())
		#RECEIVE
	

	
import system 
import java.io as F
from java.util import Calendar
c=Calendar.getInstance()
tMs=c.getTimeInMillis()
adir = "C:\\IgnitionTextFiles\\"
filename = adir+"Test_File_%d_%d.txt"%(c.get(Calendar.YEAR),c.get(Calendar.DAY_OF_YEAR))
print filename

text=log('test') 

def writeToFile(text):

    line ='\n This is %s'%(text)+'\n'
    fstream = F.FileWriter(filename,1)    
    out = F.BufferedWriter(fstream)
    out.newLine()
    out.write(line)    
    out.close()

writeToFile(text)		
