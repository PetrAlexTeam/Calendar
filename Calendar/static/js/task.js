

    function editable() {
      var h1 = document.getElementsByTagName("H1")[0];
      var p = document.getElementsByTagName("p");
      console.log(p[0])
      console.log(p[1])
      console.log(h1)
      var att = document.createAttribute("contenteditable");
      var att2 = document.createAttribute("contenteditable");
      var att3 = document.createAttribute("contenteditable");
      att.value = "true";
      att2.value = "true";
      att3.value = "true";
      h1.setAttributeNode(att);
      p[0].setAttributeNode(att2);
      p[1].setAttributeNode(att3);
    }

    function noteditable() {
      var h1 = document.getElementsByTagName("H1")[0];
      var p = document.getElementsByTagName("p");
      var att = document.createAttribute("contenteditable");
      var att2 = document.createAttribute("contenteditable");
      var att3 = document.createAttribute("contenteditable");
      att.value = "false";
      att2.value = "false";
      att3.value = "false";
      h1.setAttributeNode(att);
      p[0].setAttributeNode(att2);
      p[1].setAttributeNode(att3);
//      console.log(p[0])
//      console.log(p[1])
//      console.log(h1)
    }

    $('.my-button').click(function() {
      $(".my-textbox").focus()
    });

