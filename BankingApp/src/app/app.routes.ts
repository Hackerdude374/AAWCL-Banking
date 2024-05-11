import { Routes } from '@angular/router';
import { AuthGuard } from './service/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { SignupComponent } from './pages/signup/signup.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';

import { TransactionComponent } from './pages/transaction/transaction.component';
import { HistoryComponent } from './pages/history/history.component';
import { CardmanagementComponent } from './pages/cardmanagement/cardmanagement.component';
import { AccountComponent } from './pages/account/account.component';
import { OpenComponent } from './pages/open/open.component';

export const routes: Routes = [
    {
        path: '', redirectTo: 'login', pathMatch :'full'
    },
    {
        path: 'login',
        component:LoginComponent
    },
    {
        path: 'signup',
        component:SignupComponent
    },
    { 
        path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard]
    },
    {
        path: 'transaction', component: TransactionComponent, canActivate: [AuthGuard]
    },
    {
        path: 'history', component: HistoryComponent, canActivate: [AuthGuard]
    },
    {
        path: 'cardmanagement', component: CardmanagementComponent, canActivate: [AuthGuard]
    },
    {
        path: 'account', component: AccountComponent, canActivate: [AuthGuard]
    },
    {
        path: 'open', component: OpenComponent, canActivate: [AuthGuard]
    }
];
