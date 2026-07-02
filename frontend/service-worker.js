self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("insight-os-v1").then((cache) => {
      return cache.addAll([
        "/content-library.html",
        "/manifest.json"
      ]);
    })
  );
});
