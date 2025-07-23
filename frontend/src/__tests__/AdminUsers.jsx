import React from 'react';
import {render, screen, waitFor, fireEvent} from '@testing-library/react';
import AdminUsers from '../components/admin/AdminUsers';
import '@testing-library/jest-dom';

// Мокаем зависимости
jest.mock("../helps/logs.mjs", () => jest.fn());
jest.mock('../components/admin/AdminSendEmailModal', () => () => <div data-testid="email-modal">Modal</div>);
jest.mock('../components/admin/fetchAuth', () => ({
    fetchAuth: jest.fn()
}));

global.fetch = jest.fn();

describe('AdminUsers', () => {
    beforeEach(() => {
        fetch.mockClear();
    });

    it('Get tables with fields and update user', async () => {
        // Первый fetch: получение пользователей
        fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({
                    success: true,
                    data: {
                        users: [
                            {
                                id: 1,
                                username: 'john',
                                email: 'john@example.com',
                                phone: '123456789',
                                comments: 'test comment',
                                status: 1,
                                is_admin: 0,
                                first_name: 'John',
                                last_name: 'Doe',
                                created_at: '2025-07-22T12:00:00Z'
                            }
                        ]
                    }
                })
            })
        );

        render(<AdminUsers />);

        // Проверка загрузки пользователя
        await waitFor(() => {
            expect(screen.getByDisplayValue('john')).toBeInTheDocument();
        });

        // Изменение значения
        const usernameInput = screen.getByDisplayValue('john');
        fireEvent.change(usernameInput, { target: { value: 'johnny' } });
        expect(usernameInput.value).toBe('johnny');

        // Второй fetch: обновление пользователя
        fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({ success: true })
            })
        );

        // Третий fetch: повторное получение пользователей после update
        fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({
                    success: true,
                    data: {
                        users: [
                            {
                                id: 1,
                                username: 'johnny',
                                email: 'john@example.com',
                                phone: '123456789',
                                comments: 'test comment',
                                status: 1,
                                is_admin: 0,
                                first_name: 'John',
                                last_name: 'Doe',
                                created_at: '2025-07-22T12:00:00Z'
                            }
                        ]
                    }
                })
            })
        );

        const updateBtn = screen.getAllByTestId("item_update");
        fireEvent.click(updateBtn[0]);

        await waitFor(() => {
            const updateCall = fetch.mock.calls.find(call => call[0] === 'http://localhost:8000/user/update');
            expect(updateCall).toBeTruthy();

            const [url, options] = updateCall;

            expect(url).toBe('http://localhost:8000/user/update');
            expect(options.method).toBe('POST');
            expect(JSON.parse(options.body)).toEqual({
                username: 'johnny',
                email: 'john@example.com',
                phone: '123456789',
                comments: 'test comment',
                first_name: 'John',
                last_name: 'Doe',
            });
        });
    });
});
