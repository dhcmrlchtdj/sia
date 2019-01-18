import Typography from "typography";
import Wordpress2016 from "typography-theme-wordpress-2016";

delete Wordpress2016.googleFonts;
Wordpress2016.headerFontFamily = ["serif"];
Wordpress2016.bodyFontFamily = ["serif"];
Wordpress2016.overrideThemeStyles = () => ({ h1: { fontFamily: "serif" } });

const typography = new Typography(Wordpress2016);

// Hot reload typography in development.
if (process.env.NODE_ENV !== `production`) {
    typography.injectStyles();
}

export default typography;
export const rhythm = typography.rhythm;
export const scale = typography.scale;
