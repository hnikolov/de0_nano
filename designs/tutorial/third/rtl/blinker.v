module blinker (
    input reset,
    input clk,
    input [3:0] delay,
    output reg [7:0] led,
    input pause
);

reg [23:0] count = 24'b0;
reg [3:0]  pos   =  0;
// Pause is a switch input (not a push button)
// reg running      =  1'b0;

always @(pos) begin
    case (pos)
        4'b0000:  led <= 8'b00000001;
        4'b0001:  led <= 8'b00000010;
        4'b0010:  led <= 8'b00000100;
        4'b0011:  led <= 8'b00001000;
        4'b0100:  led <= 8'b00010000;
        4'b0101:  led <= 8'b00100000;
        4'b0110:  led <= 8'b01000000;
        4'b0111:  led <= 8'b10000000;
        4'b1000:  led <= 8'b01000000;
        4'b1001:  led <= 8'b00100000;
        4'b1010:  led <= 8'b00010000;
        4'b1011:  led <= 8'b00001000;
        4'b1100:  led <= 8'b00000100;
        4'b1101:  led <= 8'b00000010;
        default:  led <= 8'b00000000;
    endcase
end

always @(posedge clk) begin
    if( reset ) begin
        count <= 24'b0;
        pos   <=  0;
//    end else if( pause ) begin
//        running <= !running;
    end else if( !pause ) begin
        if( count == 24'b0 ) begin
            count <= { delay, 20'b0 };
            if( pos == 4'b1101 )
                pos <= 0;
            else
                pos <= pos + 1'b1;
        end else begin
            count <= count - 1'b1;
        end
    end
end

endmodule
