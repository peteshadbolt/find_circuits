/*
   pete.shadbolt@gmail.com
   This is the main JS file which runs the editor/simulator
*/

var gc, gd;
var camera, renderer, grid, circuit, mouse, editor;

// Run on startup
window.onload=main;

function Renderer(ctx, canv) {
   var self=this; 
   self.ctx=ctx;
   self.canvas=canv;
   self.change=false;

   self.loop=function () {
        setInterval(self.redraw, 17);
   }

   self.requestDraw=function () {
       requestAnimationFrame(self.redraw);
   }

   self.redraw= function () {
        if (!self.change){return;}
        self.change=false;

        // Clear canvas
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);

        // Transform into camera-space
        self.ctx.save();
        camera.contextToWorld(self.ctx);

        // Draw the grid, circuit, editor
        grid.draw(self.ctx);
        circuit.draw(self.ctx);

        // Back to screen-space
        self.ctx.restore();
    }

    self.needFrame=function () {
        self.change=true;
    }

}

function resize() {
    gc.width  = Math.floor(window.innerWidth);
    gc.height = Math.floor(window.innerHeight);
    renderer.needFrame();
}

function main() {
    // Set up the drawing environment an-d fit to window
    gc=document.getElementById('canvas');
    gd=gc.getContext('2d');

    // Create a grid, camera, and mouse
    grid=new Grid();
    camera=new Camera();
    mouse=new Mouse();
    renderer=new Renderer(gd, gc);
    mouse.bind(gd);


    // Create the circuit, simulator, and editor
    circuit = new Circuit();

    // Load the circuit which we want to display

    // Away we go
    window.onresize=resize;
    resize();
    camera.center(gc);
    camera.offset=(new Vector(100,50))
    camera.loop();
    renderer.loop();

    // Periodically reload the page
    setInterval(function() {
         var xhReq = new XMLHttpRequest();
         xhReq.open("GET", "scripts/mycircuit.js", false);
         xhReq.send(null);
         var serverResponse = xhReq.responseText;
         var q=JSON.parse(serverResponse);
         circuit.fromJSON(q);
         renderer.needFrame();
        },
         500);
}
