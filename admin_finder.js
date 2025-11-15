const axios = require("axios");
const fs = require("fs");
const colors = require("color-log");

const banner = `
██████  █    ██ ███    ███ ██████  ███    ███ ██████
██   ██ ██  ██   ████  ████ ██   ██ ████  ████ ██   ██
██████  █████    ██ ████ ██ ██████  ██ ████ ██ ██████
██      ██  ██   ██  ██  ██ ██      ██  ██  ██ ██
██      ██   ██  ██      ██ ██      ██      ██ ██
D E F 4 U L T  A D M I N  F I N D E R
`;

console.log(banner);

const baseUrl = process.argv[2];
if (!baseUrl) {
    console.log("Usage: node def4ult_admin_finder.js <target-url>");
    process.exit(1);
}

const paths = fs.readFileSync("../wordlists/admin_paths.txt", "utf-8")
    .split("\n").filter(Boolean);

(async () => {
    let found = 0;
    for (let path of paths) {
        try {
            const url = baseUrl.replace(/\/$/, "") + "/" + path.replace(/^\//, "");
            const res = await axios.get(url, { validateStatus: false, timeout: 4000 });
            if ([200, 301, 302, 403].includes(res.status)) {
                found++;
                colors.green(`[FOUND] ${url} -> ${res.status}`);
            }
        } catch {}
    }
    console.log(`[+] Scan Complete. Total Found: ${found}`);
})();
