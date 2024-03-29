# Log chat

from __future__ import print_function
import frida
import sys

session = frida.attach("PwnAdventure3-Win32-Shipping.exe")
script = session.create_script("""
         var chat = DebugSymbol.load('GameLogic.dll')
         var chat = DebugSymbol.getFunctionByName('Player::Chat');
         //var location = DebugSymbol.getFunctionByName('Player::GetLookPosition');
        let that = this;
         var playerPosMemObj = { x: 0, y: 0, z:0};
         CalculatePositionPointers();
        
         Interceptor.attach(chat, {
             onEnter: function (args) { // 0 => this; 1 => cont char* (our text)
               var chatMsg = Memory.readCString(args[0]);
                //const myString = Memory.readUtf8String(args[1]);
                
                //console.log("[chat]:" + myString.toString());
                //console.log("[Chat]: " + chatMsg);
                 //this.buf = args[1];
                 //this.len = parseInt(args[2]);
                 //log("ssl3_write(" + this.buf.toString() + ", " + this.len.toString() + ")");
                 //var bbuf = Memory.readByteArray(this.buf, this.len);
                 //console.log(chatMsg)
                 //send(args[1].toString())
                 readcommandLine(chatMsg+'')
                
             }
         });    
         
         var walkSpeed = DebugSymbol.getFunctionByName('Player::GetWalkingSpeed');
         //console.log("Player::GetWalkingSpeed() at address: " + walkSpeed);
         
         // Check Speed
         Interceptor.attach(walkSpeed,
             {
                 // Get Player * this location
                 onEnter: function (args) {
                     //console.log("Player at address: " + args[0]);
                     //this.walkingSpeedAddr = ptr(args[0]).add(120) // Offset m_walkingSpeed
                     //console.log("WalkingSpeed at address: " + this.walkingSpeedAddr);
                 },
                 // Get the return value and write the new value
                 onLeave: function (retval) {
                     //console.log("Walking Speed: " + Memory.readFloat(this.walkingSpeedAddr));
                     //Memory.writeFloat(this.walkingSpeedAddr, 9999);

                 }
             });
         
         function readcommandLine(value) {
            console.log('[chat]:' + value);
            
            if( value.split(" ")[0] == "teleport") {
              var coord = value.split(" ")[1].split(',');
              console.log(coord)
              Memory.writeFloat(playerPosMemObj['x'],parseFloat(coord[0]));
              Memory.writeFloat(playerPosMemObj['y'],parseFloat(coord[1]));
              Memory.writeFloat(playerPosMemObj['z'],parseFloat(coord[2]));
              console.log('Teleporting to location: ' + coord);
              console.log(playerPosMemObj['x'])
              console.log(playerPosMemObj['y'])
              console.log(playerPosMemObj['z'])
            } else {
            switch (value) {
            case "kill cows": 
                  console.log("Killing all cows");
                  break;
            case "teleport": 
                  console.log("Killing all cows");
                  break;   
            default:
            }
            }
         }
         
         function CalculatePositionPointers() {   
            var baseptr = Module.findBaseAddress("GameLogic.dll")
            var step1 = Memory.readPointer(ptr(baseptr).add('0x0097D7C'))
            var step2 = Memory.readPointer(ptr(step1).add('0x1C')) 
            var step3 = Memory.readPointer(ptr(step2).add('0x64')) 
            var step4 = Memory.readPointer(ptr(step3).add('0x48')) 
            var step5 = Memory.readPointer(ptr(step4).add('0x4')) 
            var step6 = Memory.readPointer(ptr(step5).add('0x288')) 
            var step7 = Memory.readPointer(ptr(step6).add('0xB4')) 
            var finalStep = ptr(step7).add('0x98')
            playerPosMemObj['x'] = ptr(ptr(finalStep).sub(8))
            playerPosMemObj['y'] = ptr(ptr(finalStep).sub(4))
            playerPosMemObj['z'] = ptr(finalStep);
            console.log(Memory.readFloat(playerPosMemObj['x']))
            console.log(Memory.readFloat(playerPosMemObj['y']))
            console.log(Memory.readFloat(playerPosMemObj['z']))
         }
         
         
         function getValueAtMemWithOffset(baseMemory, offset) {
            return Memory.readUInt(ptr((baseMemory) + offset));
         }     
 """)


def on_message(message, data):

  print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()