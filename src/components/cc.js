import React from "react";
import { rhythm } from "../utils/typography";

class CC extends React.Component {
    render() {
        return (
            <div style={{ textAlign: "right" }}>
                <a
                    href="https://creativecommons.org/licenses/by-nc-sa/4.0/"
                    style={{ fontSize: rhythm(1 / 2), fontFamily: "serif" }}
                >
                    CC BY-NC-SA 4.0
                </a>
            </div>
        );
    }
}

export default CC;
