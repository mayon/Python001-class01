alert('test')

function countUp(display) {
    var count = display.data('count') || 0;
    var div_by = 100,
        speed = Math.round(count / div_by),
        $display = display,
        run_count = 1,
        int_speed = 24;

    var int = setInterval(function() {
        if (run_count < div_by) {
            $display.text(speed * run_count);
            run_count++;
        } else if (parseInt($display.text()) < count) {
            var curr_count = parseInt($display.text()) + 1;
            $display.text(curr_count);
        } else {
            clearInterval(int);
        }
    }, int_speed);
}
console.info('test')

countUp($('.J_count'));