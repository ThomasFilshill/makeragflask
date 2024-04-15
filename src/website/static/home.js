function deleteFile(id) {
    fetch("/delete-file", {
      method: "POST",
      body: JSON.stringify({ id: id }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }