window.addEventListener('load', () => {
    const canvas = document.querySelector("#canvas");
    const context = canvas.getContext("2d");

    //Resizing
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    context.fillRect(10,10,50,60);
    context.strokeRect(60,60, 40,50);
    context.strokeStyle = "red";
    context.strokeRect(110,110, 40,50);
    context.lineWidth = 5;
    context.strokeStyle = "blue";
    context.strokeRect(120,120, 40,50);
    context.lineWidth = 2;
    context.strokeStyle = "green";
    context.strokeRect(160,120, 40,50);

    context.beginPath();
    context.moveTo(100,50);
    context.lineTo(200,50);
    context.stroke();

    context.strokeStyle = "red";
    context.beginPath();
    context.moveTo(250,50);
    context.lineTo(400,50);
    context.lineTo(400,150);
    context.stroke();

    context.strokeStyle = "blue";
    context.beginPath();
    context.moveTo(10,150);
    context.lineTo(60,150);
    context.lineTo(60,250);
    context.closePath();
    context.stroke();

    //variables
    let painting = false;

    //functions
    function startPosition(e){
        painting = true;
        context.beginPath();
        drawing(e)
    }
    function finishPosition(){
        painting = false;
        // to start drawing the second time in a new position
        // we need to
        context.closePath();
        
    }
    function drawing(e){
        //check if we are drawing or not
        if(!painting) return;        
        context.lineWidth = 6;
        context.lineCap = "round";
        context.strokeStyle = "red";

        //to start draw we need to know to where it's going
        //listening the event of the mouse position
        context.lineTo(e.clientX, e.clientY);
        context.stroke();

        // to start drawing the second time in a new position without lagging
        context.beginPath();
        context.moveTo(e.clientX, e.clientY);
    }

    //EventListeners
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', finishPosition);

    canvas.addEventListener('mousemove', drawing);


});

window.addEventListener('resize', () => {
    const canvas = document.querySelector("#canvas");
    const context = canvas.getContext("2d");

    //Resizing
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;
})