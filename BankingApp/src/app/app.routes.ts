import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { SignupComponent } from './pages/signup/signup.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { TransactionsComponent } from './pages/transactions/transactions.component';
export const routes: Routes = [
    {
        path: '', redirectTo: 'login', pathMatch :'full'
    },
    {
        path: 'login',
        component:LoginComponent
    },
    {
        path: 'dashboard',
        component:DashboardComponent
    },
    {
        path: 'signup',
        component:SignupComponent
    },
    {
        path: 'transactions',
        component:TransactionsComponent
    },
];
