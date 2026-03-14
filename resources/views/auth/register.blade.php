<x-guest-layout>
    <x-authentication-card>
        <x-slot name="logo">
            <x-authentication-card-logo />
        </x-slot>

        <x-validation-errors class="mb-4" />

        <form method="POST" action="{{ route('register') }}">
            @csrf

            <div>
                <x-label for="name" value="{{ __('Name') }}" />
                <div class="flex items-center mt-1">
                    <i class="fas fa-user text-gray-400 mr-2"></i>
                    <x-input id="name" class="block w-full" type="text" name="name" :value="old('name')" placeholder="Your Name" required autofocus autocomplete="name" />
                </div>
            </div>

            <div class="mt-4">
                <x-label for="email" value="{{ __('Email') }}" />
                <div class="flex items-center mt-1">
                    <i class="fas fa-envelope text-gray-400 mr-2"></i>
                    <x-input id="email" class="block w-full" type="email" name="email" :value="old('email')" placeholder="your@email.com" required autocomplete="username" />
                </div>
            </div>

            <div class="mt-4">
                <x-label for="phone" value="{{ __('Phone') }}" />
                <div class="flex items-center mt-1">
                    <i class="fas fa-phone text-gray-400 mr-2"></i>
                    <x-input id="phone" class="block w-full" type="text" name="phone" :value="old('phone')" placeholder="+1 (555) 000-0000" required autocomplete="phone" />
                </div>
            </div>

            <div class="mt-4">
                <x-label for="password" value="{{ __('Password') }}" />
                <div class="flex items-center mt-1">
                    <i class="fas fa-lock text-gray-400 mr-2"></i>
                    <x-input id="password" class="block w-full" type="password" name="password" placeholder="••••••••" required autocomplete="new-password" />
                </div>
            </div>

            <div class="mt-4">
                <x-label for="password_confirmation" value="{{ __('Confirm Password') }}" />
                <div class="flex items-center mt-1">
                    <i class="fas fa-lock text-gray-400 mr-2"></i>
                    <x-input id="password_confirmation" class="block w-full" type="password" name="password_confirmation" placeholder="••••••••" required autocomplete="new-password" />
                </div>
            </div>

            @if (Laravel\Jetstream\Jetstream::hasTermsAndPrivacyPolicyFeature())
                <div class="mt-4">
                    <x-label for="terms">
                        <div class="flex items-center">
                            <x-checkbox name="terms" id="terms" required />

                            <div class="ms-2">
                                {!! __('I agree to the :terms_of_service and :privacy_policy', [
                                        'terms_of_service' => '<a target="_blank" href="'.route('terms.show').'" class="underline text-sm text-gray-600 hover:text-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">'.__('Terms of Service').'</a>',
                                        'privacy_policy' => '<a target="_blank" href="'.route('policy.show').'" class="underline text-sm text-gray-600 hover:text-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">'.__('Privacy Policy').'</a>',
                                ]) !!}
                            </div>
                        </div>
                    </x-label>
                </div>
            @endif

            <div class="flex items-center justify-end mt-4">
                <a class="underline text-sm text-gray-600 hover:text-gray-900 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" href="{{ route('login') }}">
                    {{ __('Already registered?') }}
                </a>

                <x-button class="ms-4">
                    <i class="fas fa-user-plus mr-2"></i>{{ __('Register') }}
                </x-button>
            </div>
        </form>
    </x-authentication-card>
</x-guest-layout>
