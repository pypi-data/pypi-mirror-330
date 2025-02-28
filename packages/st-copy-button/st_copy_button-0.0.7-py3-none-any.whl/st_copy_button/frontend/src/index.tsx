import { RenderData } from "streamlit-component-lib";

// Define the Streamlit API directly
function sendMessageToStreamlitClient(type: string, data: any) {
  console.log(type, data);
  const outData = Object.assign(
    {
      isStreamlitMessage: true,
      type: type,
    },
    data
  );
  window.parent.postMessage(outData, "*");
}

const StreamlitAPI = {
  setComponentReady: function () {
    sendMessageToStreamlitClient("streamlit:componentReady", { apiVersion: 1 });
  },
  setFrameHeight: function (height: number) {
    sendMessageToStreamlitClient("streamlit:setFrameHeight", { height });
  },
  setComponentValue: function (value: any) {
    sendMessageToStreamlitClient("streamlit:setComponentValue", { value });
  },
  RENDER_EVENT: "streamlit:render",
  events: {
    addEventListener: function (type: string, callback: (event: CustomEvent) => void) {
      window.addEventListener("message", function (event: MessageEvent) {
        if (event.data.type === type) {
          (event as any).detail = event.data;
          callback(event as unknown as CustomEvent);
        }
      });
    },
  },
};

// Copy button logic
const span = document.body.appendChild(document.createElement("span"));
const textElement = span.appendChild(document.createElement("button"));
const button = span.appendChild(document.createElement("button"));

textElement.className = "st-copy-button";
button.className = "st-copy-button";

let windowRendered = false;

function onRender(event: Event): void {
  if (!windowRendered) {
    const data = (event as CustomEvent<RenderData>).detail;
    const { text, before_copy_label, after_copy_label, show_text } = data.args;

    button.textContent = before_copy_label;

    if (show_text) {
      textElement.textContent = text;
      textElement.style.display = "inline";
    } else {
      textElement.style.display = "none";
    }

    const copyToClipboard = function () {
      navigator.clipboard.writeText(text);
      button.textContent = after_copy_label;
      StreamlitAPI.setComponentValue(true);
      setTimeout(() => {
        if (!button) return;
        button.textContent = before_copy_label;
      }, 1000);
    };

    button.addEventListener("click", copyToClipboard);
    textElement.addEventListener("click", copyToClipboard);

    windowRendered = true;
  }
  StreamlitAPI.setFrameHeight(40);
}

StreamlitAPI.events.addEventListener(StreamlitAPI.RENDER_EVENT, onRender);
StreamlitAPI.setComponentReady();
StreamlitAPI.setFrameHeight(40);
