function runIntel(program){
    var ramSize=4096;
    var ram = Array.from(Array(ramSize)).map((arg,index)=>0);

    var i=0;

    for(let instruction of program){
        ram[i] = instruction;
        i++
    }

    i=4001;

    for(let c of "flag{XXXXXXXXXXXXX}"){
        ram[i] = c.charCodeAt(0);
        i++
    }

    var registers=[0,0,0,0,0,0,0,0];

    var instructions=[
        (a0,a1,a2)=>{},
        (a0,a1,a2)=>{
            if(a1<4000)
                registers[a0] = ram[a1]
        },
        (a0,a1,a2)=>console.log(String.fromCharCode(registers[a0])), // 2
        (a0,a1,a2)=>registers[a0]=registers[a1]-registers[a2], // SUB Registers
        (a0,a1,a2)=>registers[a0]=registers[a1]+registers[a2], // ADD Registers
        (a0,a1,a2)=>{
            if(a0<4000)
                ram[a0]=registers[a1]
        },
        (a0,a1,a2)=>console.log(registers), // 6: Print registers
        (a0,a1,a2)=>registers[a0]=a1,
        (a0,a1,a2)=>registers[a0]=ram[a1]+ram[a2] // 8: ADD ram values
    ];

    i=0;

    while(i+3<=4000){
        if(instructions[ram[i]]!==undefined)
            instructions[ram[i]](
                ram[i+1],
                ram[i+2],
                ram[i+3]
            );
        i+=4
    }
}
process.stdin.on('data',function(oo){
    let o = String(oo).split(" ");
    o=o.map(ooo=>parseInt(ooo));
    runIntel(o)
});

console.log("Welcome to intel_3.js! Good luck with this one smarty pants")
