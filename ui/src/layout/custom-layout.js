import { Layout } from 'react-admin';

import CustomMenu from './custom-menu';

const CustomLayout = (props) => <Layout {...props} menu={CustomMenu} />;

export default CustomLayout;