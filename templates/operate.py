<!DOCTYPE html>
<html>
<head>
  <title>TrafficLight Control Center</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
  * {
    box-sizing: border-box;
  }
  .menu {
    float:left;
    width:50%;
    text-align:center;
  }
  .menu a {
    background-color:#e5e5e5;
    padding:1px;
    margin-top:3px;
    display:block;
    width:100%;
    color:black;
  }
  .main {
    float:left;
    width:50%;
    padding:0 20px;
  }

  @media only screen and (max-width:800px) {
    /* For mobile phones: */
    .menu, .main {
      width:100%;
    }
  }
  </style>
</head>
<body style="font-family:Verdana;color:#aaaaaa;">

  <div style="background-color:#e5e5e5;padding:1px;text-align:center;">
    <h1>School Traffic Light</h1>
  </div>

  <div style="overflow:auto">
    <div class="menu">
      <a href="/Auto"><h2><i>Auto</i></h2></a>
      <a href="/Manual1"><h2><i>Manual 1</i></h2></a>
      <a href="/Manual2"><h2><i>Manual 2</i></h2></a>
      <a href="/Standby"><h2><i>Standby</i></h2></a>
    </div>
    <div class="main">
      <h2>Status</h2>
        <p>{{prog}}{{rMode}}{{note}}</p>
        <p><b>Network</b> {{ipAddr}}</p>
      </div>
    </div>
    <div style="background-color:#e5e5e5;text-align:center;padding:10px;margin-top:5px;">© copyright</div>

    <div style="background-color:orange; text-align:center; padding:1px; margin-top:5px;">
      <a style="color:white;" href="/Shutdown"><h2>Shutdown</h2></a>
  </div>

</body>
</html>