/*
   pete.shadbolt@gmail.com
   Keeps track of the position of the camera. The camera's position is defined relative to the WORLD, not the SCREEN
*/

function Camera()
{
    var self=this;
    self.pos=new Vector(0, 0);
    self.offset=new Vector(0, 0);
    self.z=45; self.tz=45;

    self.translate = function (delta) {
        self.pos.inc(delta);
    }

    self.zoom = function (dz) {
        self.tz+=dz;
        if (self.tz<5) {self.tz=5};
        if (self.tz>200) {self.tz=200};
    }

    self.center = function (canvas) {
        self.offset.set(canvas.width/2, canvas.height/2);
    }

    // Map a context to the world space
    self.contextToWorld = function (ctx) {
        ctx.translate(self.pos.x+self.offset.x, self.pos.y+self.offset.y);
        ctx.scale(self.z, self.z);
    }

    // Mapping between the screen and the world
    self.fromScreen = function(screenPos) {
        return new Vector((screenPos.x - self.offset.x - self.pos.x)/self.z,
                        (screenPos.y - self.offset.y - self.pos.y)/self.z);
    }

    // Alias the above function
    self.toWorld=self.fromScreen; 

    // Check to see whether we need to do a smooth zoom
    self.loop = function () {
        setInterval(self.update, 16);
    }

    // For smooth zooming and targeting
    self.update = function () {
        if (Math.abs(self.z-self.tz)>1) {
            // Store the position of the mouse
            var temp1 = self.fromScreen(mouse.screenPos);
            self.z+=(self.tz-self.z)*.4
            //That position should not change after the zoom
            var temp2 = self.fromScreen(mouse.screenPos);
            self.pos.x+=(temp2.x-temp1.x)*self.z;
            self.pos.y+=(temp2.y-temp1.y)*self.z;
            renderer.needFrame();
        }
    }
}

