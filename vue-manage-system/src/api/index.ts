import request from '../utils/request';

export const fetchData = () => {
    return request({
        url: './mock/table.json',
        method: 'get'
    });
};

export const fetchUserData = () => {
    return request({
        url: '/api/dealing',
        method: 'get'
    });
};
export const fetchDealingDataMerge = () => {
    return request({
        url: '/api/dealing',
        method: 'get',
        params: { type: 1 }
    });
};
export const fetchRoleData = () => {
    return request({
        url: './mock/role.json',
        method: 'get'
    });
};
