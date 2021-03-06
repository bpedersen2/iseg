["test/Erwin/HV-IntelligentPowersupply"]
type = "iseg.CC2x.IntelligentPowerSupply"
address = '172.25.25.56'
user = 'admin'
password = 'password'
absmin = 0 
absmax = 0
tripeventallmodulesoff = 0

transitions="""
{
"TRANSITION" :[
{"goOn":  [
              {"GROUP":["Window"],"Control.clearAll": [1]},
			  {"GROUP":["Anodes"],"Control.clearAll": [1,1,1]},
			  {"GROUP":["CathodeStripes"],"Control.clearAll": [1,1]},
              {"GROUP":["Window"],"Control.voltageSet": [-40]},
              {"GROUP":["Window"],"Control.on": [1] },
              {"GROUP":["Window"],"Status.ramping": [0] },
              {"GROUP":["Anodes"],"Control.voltageSet": [75,100,85]},
              {"GROUP":["Anodes"],"Control.on": [1,1,1] },
              {"GROUP":["CathodeStripes"],"Control.voltageSet": [75,80]},
              {"GROUP":["CathodeStripes"],"Control.on": [1,1]},
              {"GROUP":["CathodeStripes"],"Status.ramping": [0,0]},
              {"GROUP":["Anodes"],"Status.ramping": [0,0,0] }
             ]
},
{"goOff":  [
             {"GROUP":["Anodes"],"Control.on": [0,0,0] } ,
             {"GROUP":["Anodes"],"Status.ramping": [0,0,0] },
             {"GROUP":["CathodeStripes"],"Control.on": [0,0]},
             {"GROUP":["Window"],"Control.on": [0] },
             {"GROUP":["Window"],"Status.ramping": [0] },
             {"GROUP":["CathodeStripes"],"Status.ramping": [0, 0]}
            ]
},
{"goMoving":  [
              {"GROUP":["Anodes"],"Control.voltageSet": [65,60,70]},
              {"GROUP":["Anodes"],"Status.ramping": [0,0,0] }
             ]
}
]
}
"""

groups="""
{
 "GROUP": [
   {"Module0": { "CHANNEL": ["0_0"], "Control.on": 1, "Control.kill": 0, "Control.voltageRampspeed" : 0.17 }},
   {"Module1": { "CHANNEL": ["0_1"], "Control.on": 1,"Control.kill": 0, "Control.voltageRampspeed" : 0.17 }},
   {"Window": { "CHANNEL": ["0_1_7"], "OPERATINGSTYLE": "normal" }},
   {"Anodes": { "CHANNEL": ["0_1_0","0_1_1","0_1_2"]  ,"OPERATINGSTYLE": "normal" }},
   {"CathodeStripes": { "CHANNEL": ["0_1_4","0_1_5"],  "OPERATINGSTYLE": "slow" }}
 ]
}
"""
operatingstyles="""
{
  "OPERATNGSTYLE":
  [
    {"normal": {
	            "Control.clearAll" : 1 ,
                "Control.currentSet" : 1.5,
                "Setup.delayedTripTime" : 500,
				"Setup.delayedTripAction" : 2
     }},
	 {"slow": {
	            "Control.clearAll" : 1 ,
                "Control.currentSet" : 3,
                "Setup.delayedTripTime" : 800,
				"Setup.delayedTripAction" : 2
	 }}
   ]
}
"""
