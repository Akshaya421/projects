/* let today= new Date();
            let h=today.getHours();
            let m=today.getMinutes();
            let s=today.getSeconds();
            let dh=document.getElementById('hour');
            let dm=document.getElementById('minute');
            let ds=document.getElementById('second');
            dh.innerHTML=h;
            dm.innerHTML=m;
            ds.innerHTML=s;
        
*/
function displayTime() {
    let today = new Date();

    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
        let ampm = h >= 12 ? "PM" : "AM";

    // Convert 24-hour format to 12-hour format
    h = h % 12;
    h = h ? h : 12; // 0 becomes 12

    // Add leading zeros
    h = String(h).padStart(2, '0');
    m = String(m).padStart(2, '0');
    s = String(s).padStart(2, '0');

    document.getElementById("hour").innerHTML = h;
    document.getElementById("minute").innerHTML = m;
    document.getElementById("second").innerHTML = s;
    document.getElementById("ampm").innerHTML = ampm;
}

// Run immediately
displayTime();

// Update every second
setInterval(displayTime, 1000);

    