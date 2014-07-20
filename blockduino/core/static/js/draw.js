function() {
    /* Canvas must be 300 x 300
    <canvas id="board_canvas" width="300" height="300"></canvas>
    */
    /* The bottom most actuating/sensing pin the module is connected to

            3       6
            2       5
            1       4
    
     */
    
    function getXY(corner) {
        if (corner == '1'){
            return [26, 204];
        } else if (corner == '2') {
            return [26, 142];
        } else if (corner == '3') {
            return [26, 80];
        } else if (corner == '4') {
            return [212, 80];
        } else if (corner == '5') {
            return [212, 142];
        } else if (corner == '6') {
            return [212, 204];
        }
    };
    
    function drawAccelerometer(corner, ctx) {
        ctx.fillStyle == 'red';
        c1 = getXY(corner);
        ctx.fillRect(c1[0], c1[1], c1[0] + 62, c1[1] - 62);

        ctx.fillRect(c1[0], c1[1] - 62, c1[0] + 62, c1[1] - 124);
        return;
    };

    function drawLED(corner, ctx) {
        ctx.fillStyle == 'blue';
        c1 = getXY(corner)

        ctx.fillRect(c1[0], c1[1], c1[0] + 62, c1[1] - 62);
    };

    function drawServo(corner, ctx) {
        ctx.fillStyle == 'orange';
        c1 = getXY(corner)

        ctx.fillRect(c1[0], c1[1], c1[0] + 62, c1[1] - 62);
    };

    function drawPush(corner, ctx) {
        ctx.fillStyle == 'black';
        c1 = getXY(corner)

        ctx.fillRect(c1[0], c1[1], c1[0] + 62, c1[1] - 62);
    };


    var canvas = document.getElementById('board_canvas');
    if (canvas.getContext) {
        var ctx = canvas.getContext('2d');

        /* DRAW APPROPRIATE MODULE PASSING IN CORNER AND CTX */
    }
}
