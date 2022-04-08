# Stimulator class

# Imports
#from StimulationSignal import StimulationSignal


import crccheck.checksum
import numpy as np
import serial
import time
import struct



# channel_stim:   list of active channels
# freq:           main stimulation frequency in Hz (NOTE: this overrides ts1)
# ts1:            main stimulation period in ms (1-1024.5 ms in 0.5 steps)
# ts2:            inter-pulse time in ms (1.5-17 ms in 0.5 steps)

# Notes:
# - Revoir les principes d'orienté objet (encapsulation)
# - Indentation : 4 espaces

class Stimulator:

    # Class variables
    VERSION = 0x01

    INIT_REPETITION_TIME = 0.5


    START_BYTE = 0xF0
    STOP_BYTE  = 0x0F
    STUFFING_BYTE = 0x81
    STUFFING_KEY = 0x55
    MAX_PACKET_BYTES = 69

    BAUD_RATE = 460800

    TYPES = {'Init': 0x01, 'InitAck': 0x02, 'UnknownCommand': 0x03, 'Watchdog': 0x04,
             'GetStimulationMode': 0x0A, 'GetStimulationModeAck': 0x0B,
             'InitChannelListMode': 0x1E, 'InitChannelListModeAck': 0x1F,
             'StartChannelListMode': 0x20, 'StartChannelListModeAck': 0x21,
             'StopChannelListMode': 0x22, 'StopChannelListModeAck': 0x23,
             'SinglePulse': 0x24, 'SinglePulseAck': 0x25, 'StimulationError': 0x26}


    # Constuctor
    def __init__(self, ts2, StimulationSignal, port_path): #Changer ts1 pour 1/StimulationSignal.frequency
    # ---- StimulationSignal = Contient les infos d'amplitude, de fréquence, de durée d'impulsion et le nom du muscle pour chaque électrode ---- #
    # ---- ts1 = Main stimulation interval                                 ---- #
    # ---- ts2 = Inter pulse interval (use only if use duplet or triplet)  ---- #
    # ---- Mode = Single pulse, duplet or triplet                          ---- #
    # ---- port = open port from port_path                                 ---- #
    # ---- packet_count = initialise the packet count                      ---- #

        self.StimulationSignal = StimulationSignal
        self.electrode_number = 0
        idx = []
            
        for i in range(0,8):
            if StimulationSignal[0][i]==0:
                idx.append(i)
                
            else:
                self.electrode_number += (2)**(i)
        StimulationSignal = np.delete(StimulationSignal, idx, 1)


        self.amplitude = StimulationSignal[0] #à vérifier si bon indice
        
# Generate an error
        self.ts1 = int((1000/StimulationSignal[1] - 1)/0.5) #à vérifier si bon indice pour fréquence
        self.frequency = StimulationSignal[1]
        self.pulse_width = StimulationSignal[2] #à vérifier si bon indice
        self.muscle = StimulationSignal[3]
        self.ts2 = ts2
        self.port = serial.Serial(port_path, self.BAUD_RATE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.1)
        self.packet_count = 0
<<<<<<< HEAD
        
=======
>>>>>>> parent of 9b1fd77 (Works with matrix from UI)

        """
        while True:
            received_packet= self.read_packets()
            self.init_ACK(received_packet)
            time.sleep(self.INIT_REPETITION_TIME)
        return"""
        while (1):
            if (self.port.in_waiting>0):
                self.calling_ACK()
                break
<<<<<<< HEAD
        self.set_stim_biceps_DeltPost() 
        print(self.set_stim_biceps_DeltPost())
        starttime = time.time()
        timer = 0
        self.send_packet('InitChannelListMode', self.packet_count)
        while timer < 5.00:
            timer = round(time.time()-starttime,2)
            self.send_packet('StartChannelListMode', self.packet_count)
            time.sleep(1/self.frequency[0])
            if timer >=(5.00-(1/self.frequency[0])):
                break
            
       
=======
            
        self.send_packet('InitChannelListMode',5, self.packet_count)
        #self.send_packet('InitChannelListMode',2, self.packet_count)
        self.send_packet('GetStimulationMode',1,self.packet_count)
        for i in range (5):
            self.send_packet('StartChannelListMode',1, self.packet_count)
        print(self.read_packets())
>>>>>>> parent of 9b1fd77 (Works with matrix from UI)
        
        
        
    # Function to modify the stimulation's parameters
    def set_StimulationSignal(self,StimulationSignal):
        self.StimulationSignal = StimulationSignal
        self.amplitude = StimulationSignal[0] #à vérifier si bon indice
        self.ts1 = 1/StimulationSignal[1] #à vérifier si bon indice pour avoir fréquence
        self.pulse_width = StimulationSignal[2] #à vérifier si bon indice
        self.muscle = StimulationSignal[3]

    def set_stim_biceps_DeltPost(self):
        idx = []
        biceps_DeltPost = np.copy(self.StimulationSignal)
        for j in range(np.shape(self.StimulationSignal)[1]): 
            
            if(self.StimulationSignal[3][j] == 1 or self.StimulationSignal[3][j]== 3):
                biceps_DeltPost[:,j]=0
                
        for i in range(0,8):
            print(biceps_DeltPost[0][i])
            if biceps_DeltPost[0][i]==0:
                idx.append(i)
                
            else:
                self.electrode_number += (2)**(i)
        biceps_DeltPost = np.delete(biceps_DeltPost, idx, 1)
                
        self.StimulationSignal = biceps_DeltPost
    
    def set_stim_triceps_DeltAnt(self):
        idx = []
        triceps_DeltAnt = np.copy(self.StimulationSignal)
        for j in range(np.shape(self.StimulationSignal)[1]): 
            
            if(self.StimulationSignal[3][j] == 1 or self.StimulationSignal[3][j]== 3):
                triceps_DeltAnt[:,j]=0
                
        for i in range(0,8):
            if triceps_DeltAnt[0][i]==0:
                idx.append(i)
                
            else:
                self.electrode_number += (2)**(i)
        triceps_DeltAnt = np.delete(triceps_DeltAnt, idx, 1)
                
        self.StimulationSignal = triceps_DeltAnt
                

    # Function to modify the time between pulses if doublet or triplet are chose
    def set_t2(self,t2):
        self.t2 = t2


    # "byte stuffing", i.e, xoring with STUFFING_KEY
    def stuff_byte(self,byte):
        return ((byte & ~Stimulator.STUFFING_KEY) | (~byte & Stimulator.STUFFING_KEY))
        #return bytes(a ^ b for (a, b) in zip(byte, bitarray(self.STUFFING_KEY)))

    # Construction of each packet
    def packet_construction(self,packet_count, packet_type, *packet_data):
        start_byte = self.START_BYTE
        stop_byte = self.STOP_BYTE
        self.packet_type = packet_type
        packet_command = self.TYPES[packet_type]
        packet_payload = [packet_count, packet_command]  
        data_length = 0
        if packet_data!= None:
            packet_data = list(packet_data)
            
            for i in range (0, len(packet_data)):
                if packet_data[i] == 240 or packet_data[i] == 15:
                    packet_data[i] = self.stuff_byte(packet_data[i])
            packet_payload += packet_data
        
        checksum = crccheck.crc.Crc8.calc(packet_payload)
        checksum = self.stuff_byte(checksum)
        data_length = self.stuff_byte(len(packet_payload))
        
        packet_lead = [start_byte, self.STUFFING_BYTE, checksum, self.STUFFING_BYTE, data_length]
        packet_end = [stop_byte]
        packet = packet_lead + packet_payload + packet_end
        
        return b''.join([byte.to_bytes(1, 'little') for byte in packet])


# Closes port
    def close_port(self):
        self.port.close()

# Send packets
    def send_packet(self, cmd, packet_number):
        if cmd == 'InitAck':
            self.port.write(self.init_ACK(packet_number))
        elif cmd == 'Watchdog':
            self.port.write(self.watchdog())
        elif cmd == 'GetStimulationMode':
            self.port.write(self.getMode())
        elif cmd == 'InitChannelListMode':
            self.port.write(self.init_stimulation()) #quoi faire avec channel_execution
        elif cmd == 'StartChannelListMode':
            self.port.write(self.start_stimulation())
        elif cmd == 'StopChannelListMode':
            self.port.write(self.stop_stimulation())
        # Update packet count
        self.packet_count = (self.packet_count + 1) % 256

# Receives packet
    # Read the received packet
    def read_packets(self):

        # Read port stream
        packet = self.port.readline()
        # If it is a start byte, collect packet
        if packet[0] == self.START_BYTE:
            # Collect header bytes
            ''' for i in range(4):
                packet += self.port.read()
            # Collect data bytes
            datalength = packet[-1]
            for i in range(datalength):
                packet += self.port.read()
            # Collect stop byte
            packet += self.port.read()
            # Call the right ACK function '''
            return packet
        else:
            # Return empty string to avoid hanging
            return b''

# Creates packet for every command part of dictionary TYPES
    def calling_ACK(self):
            #Call the Ack function
        packet = self.read_packets()
        if(int(packet[6]) == Stimulator.TYPES['Init'] and int(packet[7]) == self.VERSION):
<<<<<<< HEAD
            
            return Stimulator.send_packet(self, 'InitAck', int(packet[5]))
=======
            print((packet[5]), 'packet_number recu')
            print(packet[0], packet[1],packet[2], packet[3], packet[4], packet[5], packet[6], packet[7], packet[8])
            return Stimulator.send_packet(self, 'InitAck', 1, int(packet[5]))
>>>>>>> parent of 9b1fd77 (Works with matrix from UI)
        elif(str(packet[6]) == Stimulator.TYPES['UnknownCommand']):
            return Stimulator.unknown_cmd()
        elif(str(packet[6]) == Stimulator.TYPES['GetStimulationModeAck']):
            return Stimulator.getmodeACK(packet)
        elif(str(packet[6]) == Stimulator.TYPES['InitChannelListModeAck']):
            return Stimulator.init_stimulation_ACK(packet)
        elif(str(packet[6]) == Stimulator.TYPES['StartChannelListMode']):
            return Stimulator.start_stimulation_ACK(packet)
        elif(str(packet[6]) == Stimulator.TYPES['StopChannelListModeAck']):
            return Stimulator.stop_stimulation_ACK(packet)
        elif(str(packet[6]) == Stimulator.TYPES['StartChannelListModeAck']):
            return Stimulator.error_stimulation_ACK(packet)
    # Establishes connexion acknowlege
    def init(self, packet_count):
        packet = self.packet_construction(packet_count,'Init', self.VERSION )
        return packet

    # Establishes connexion acknowlege
    def init_ACK(self, packet_count):
        packet = self.packet_construction(packet_count, 'InitAck', 0)
        
        return packet



    # Sends message for unknown command
    def unknown_cmd(self, packet):
        return str(packet[6])


    # Error signal (inactivity ends connexion)  VERIFY IF IT HAVE TO BE SEND EVERY <1200MS OR SEND IF ONLY NOTHING SEND AFTER 120MS
    def watchdog(self):
        packet = self.packet_construction(self.packet_count,'Watchdog')
        return packet


    # Asking to know which mode has been chosen
    def getMode(self):
        packet = self.packet_construction(self.packet_count, 'GetStimulationMode')
        return packet


    # Sent by RehaStim2 in response to getMode
    def getModeACK(self, packet):

        if(str(packet[6] == '0')):
            if(str(packet[7]) == '0'):
                return 'Start Mode'
            elif(str(packet[7]) == '1'):
                return 'Stimulation initialized'
            elif(str(packet[7]) == '2'):
                return 'Stimulation started'
        elif(str(packet[6]) == '-1'):
            return 'Transfer error'
        elif(str(packet[6]) == '-8'):
            return 'Busy error' #add a timer


    # Initialises stimulation
    def init_stimulation(self):
        #max_frequency = max(self.StimulationSignal[1])
       # max_frequency_electrode = np.where(self.StimulationSignal[1]==max_frequency)
       # low_frequency_electrode = np.where(self.StimulationSignal[1]!=max_frequency)
        print (self.ts1, "TS1")
        MSB, LSB = self.MSB_LSB_main_stim()
        packet = self.packet_construction(self.packet_count,'InitChannelListMode', 0, self.electrode_number, 0, 2, MSB, LSB, 0 ) # Channel est 1,2,4,8,16,32,64,128 pour chaque et l'addition donne l'activation de plusieurs channels
        return packet


    # Sent by RehaStim2 in response to init_stimulation
    def init_stimulation_ACK(self, packet):

            if(str(packet[6]) == '0'):
                return 'Stimulation initialized'
            elif(str(packet[6]) == '-1'):
                return 'Transfer error'
            elif(str(packet[6]) == '-2'):
                return 'Parameter error' #Change for please change parameters?
            elif(str(packet[6]) == '-3'):
                return 'Wrong mode error'
            elif(str(packet[6]) == '-8'):
                return 'Busy error' # Add a timer?

    # Starts stimulation and modifies it
    def start_stimulation(self): #VA PROBABLEMENT CHANGER PULSE_WIDTH ET AMPLITUDE SELON COMMENT RÉCUPÈRE DONNÉES
        #if len(self.pulse_width) == 1:
<<<<<<< HEAD
        MSB_matrix =[]
        LSB_matrix =[]
        for i in range (len(self.amplitude)):
            MSB, LSB = self.MSB_LSB_pulse_stim(self.pulse_width[i])
            MSB_matrix.append(MSB)
            LSB_matrix.append(LSB)
        
        if (len(self.amplitude)) ==1:

            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, int(MSB_matrix[0]), int(LSB_matrix[0]), int(self.amplitude[0]))
        if len(self.amplitude) == 2:
=======
        #for i in range (len(StimulationSignal)):
        #    MSB[i], LSB[i] = self.MSB_LSB_pulse_stim()
        packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, 0, 15, 100, 0, 1, 240, 100)
        ''' if len(self.pulse_width) == 2:
>>>>>>> parent of 9b1fd77 (Works with matrix from UI)
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1])
        elif len(self.pulse_width) == 3:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2])
        elif len(self.pulse_width) == 4:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2],
                                              0, self.pulse_width[3], None, self.amplitude[3])
        elif len(self.pulse_width) == 5:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2],
                                              0, self.pulse_width[3], None, self.amplitude[3],
                                              0, self.pulse_width[4], None, self.amplitude[4])
        elif len(self.pulse_width) == 6:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2],
                                              0, self.pulse_width[3], None, self.amplitude[3],
                                              0, self.pulse_width[4], None, self.amplitude[4],
                                              0, self.pulse_width[5], None, self.amplitude[5])
        elif len(self.pulse_width) == 7:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2],
                                              0, self.pulse_width[3], None, self.amplitude[3],
                                              0, self.pulse_width[4], None, self.amplitude[4],
                                              0, self.pulse_width[5], None, self.amplitude[5],
                                              0, self.pulse_width[6], None, self.amplitude[6])
        elif len(self.pulse_width) == 8:
            packet = self.packet_construction(self.packet_count,'StartChannelListMode',
                                              0, self.pulse_width[0], None, self.amplitude[0],
                                              0, self.pulse_width[1], None, self.amplitude[1],
                                              0, self.pulse_width[2], None, self.amplitude[2],
                                              0, self.pulse_width[3], None, self.amplitude[3],
                                              0, self.pulse_width[4], None, self.amplitude[4],
                                              0, self.pulse_width[5], None, self.amplitude[5],
                                              0, self.pulse_width[6], None, self.amplitude[6],
                                              0, self.pulse_width[7], None, self.amplitude[7])
 '''
        return packet

    # Sent by RehaStim2 in response to start_stimulation
    def start_stimulation_ACK(self, packet):

        if(str(packet[6]) == '0'):
            return ' Stimulation started'
        if(str(packet[6]) == '-1'):
            return ' Transfer error'
        if(str(packet[6]) == '-2'):
            return ' Parameter error'
        if(str(packet[6]) == '-3'):
            return ' Wrong mode error'
        if(str(packet[6]) == '-8'):
            return ' Busy error'


    # Stops stimulation
    def stop_stimulation(self):
        packet = self.packet_construction(self.packet_count,Stimulator.TYPES['StopChannelListMode'])
        return packet


    # Sent by RehaStim2 in response to stop_stimulation
    def stop_stimulation_ACK(self, packet):

        if(str(packet[6]) == '0'):
            return ' Stimulation stopped'
        elif(str(packet[6]) == '-1'):
            return ' Transfer error'


    def stimulation_error(self, packet):

        if(str(packet[6]) == '-1'):
            return ' Emergency switch activated/not connected' #mettre fonction qui affiche message sur interface
        elif(str(packet[6]) == '-2'):
            return ' Electrode error'
        elif(str(packet[6]) == '-3'):
            return 'Stimulation module error'

    ''' 
    def testing_stimulation(self, electrode_number): # lié avec +- courant
        self.ts1 = 3 #à vérifier
        self.send_packet('InitChannelListMode', electrode_number)
        received_packet=self.read_packets()
        if (received_packet == 'Stimulation initialized'):
            self.send_packet('StartChannelListMode', electrode_number)
            received_packet = self.read_packets()
            if (received_packet == 'busy error'):
                while():
                    time.sleep(10)
                self.send_packet('StartChannelListMode')
            elif (received_packet == 'transfer error'):
                self.send_packet('StartChannelListMode')
            #elif (received_packet == 'Wrong mode error'):
                #self.mode ==
            #elif (received_packet == 'Parameter error'): '''

        ''' def control_stimulation(self, electrode_number): #lié avec bouton start stim/update ET position pédalier
        self.send_packet('InitChannelListMode', electrode_number)
        received_packet=self.read_packets()

        if (received_packet == 'Stimulation initialized'):
            self.send_packet('StartChannelListMode', electrode_number)
            received_packet = self.read_packets()
            if (received_packet == 'busy error'):
                while():
                    time.sleep(10)
                self.send_packet('StartChannelListMode')
            elif (received_packet == 'transfer error'):
                self.send_packet('StartChannelListMode')
            #elif (received_packet == 'Wrong mode error'):
                #self.mode ==
            #elif (received_packet == 'Parameter error'): '''


      # Function to command the stimulator with pre-defined commands
    def throw_command(self, command):
        print("(Stimulator) TODO : call the '" + command + "' command")

        #if command type == hexadécimal of certain command, throw associated function.
        #fonction qui lit le paquet reçu par rehastim et qui l'associe à une commande.

        #command = {'Init':0x01}

    def MSB_LSB_main_stim (self):
        if self.ts1 <= 255:
            LSB = self.ts1
            MSB = 0;
        elif 256 <= self.ts1 <= 511:
            LSB = self.ts1-256
            MSB = 1;
        elif 512 <= self.ts1 <= 767:
            LSB = self.ts1-512
            MSB = 2;   
        elif 768 <= self.ts1 <= 1023:
            LSB = self.ts1-768
            MSB = 3;    
        elif 1024 <= self.ts1 <= 1279:
            LSB = self.ts1-1024
            MSB = 4;   
        elif 1280 <= self.ts1 <= 1535:
            LSB = self.ts1-1280
            MSB = 5;  
        elif 1536 <= self.ts1 <= 1791:
            LSB = self.ts1-1536
            MSB = 6;  
        elif 1792 <= self.ts1 <= 2047:
            LSB = self.ts1-1792
            MSB = 7;  
        elif self.ts1 == 2048:
            LSB = 0
            MSB = 8; 

        return MSB, int(LSB)


    def MSB_LSB_pulse_stim (self):
        if self.pulse_width <= 255:
            LSB = self.pulse_width
            MSB = 0;
        elif 256 <= self.pulse_width <= 500:
            LSB = self.pulse_width-256
            MSB = 1;
        return MSB,int(LSB)
    '''
    if (InstructionWindow.clicked_started()): #changer pour ouverture
            Stimulator.send_packet('Init')
            Stimulator.read_packets()
        if (Stimulator.read_packets() == 'Connexion established'):
            Stimulator.send_packet('InitChannelListMode')
            if(Stimulator.read_packets() == 'Stimulation initialized'):
                if()
    Vérifier si utile pour nous ou si décide de le faire pour plus tard

    # Sends a unique impulsion
    def single_pulse():
        print("TODO")


    # Sent by RehaStim2 in response to single_pulse
    def single_pulse_ACK():
        print("TODO")

    POSSIBLEMENT PAS UNE COMMANDE EN SOI

    # Error message sent by RehaStim2
    def error():
        print("TODO")

    '''
