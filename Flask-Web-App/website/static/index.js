function refreshWallet() {
  fetch("/refresh", {
    method: "POST",
    body: JSON.stringify({}),
  }).then((_res) => {
    window.location.href = "/";
  });
}
